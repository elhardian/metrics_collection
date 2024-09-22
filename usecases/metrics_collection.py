import time
from functools import wraps

from pydantic import BaseModel
from sqlalchemy import func
from intergrations.queue.collection_consumer import collection_queue
from intergrations.database import SessionManager
from models.metric import Metric

def capture_execution():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time() 
            is_error = False
            try:
                result = await func(*args, **kwargs) 
            except Exception as err: 
                is_error = True
            end_time = time.time() 
            execution_time = end_time - start_time

            await collection_queue.put({
                "execution_time": execution_time, 
                "function_name": func.__name__,
                "is_error": is_error
            })
            return result
        return wrapper
    return decorator