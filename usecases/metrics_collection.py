import time
from functools import wraps
from intergrations.queue.collection_consumer import collection_queue

def capture_execution():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time() 
            result = await func(*args, **kwargs) 
            end_time = time.time() 
            execution_time = end_time - start_time

            await collection_queue.put({
                "execution_time": execution_time, 
                "function_name": func.__name__
            })
            return result
        return wrapper
    return decorator