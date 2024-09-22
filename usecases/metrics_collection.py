import time
from functools import wraps

from pydantic import BaseModel
from sqlalchemy import func
from intergrations.database import SessionManager
from models.metric import Metric

def capture_execution():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from intergrations.queue.collection_consumer import collection_queue
            start_time = time.time() 
            is_error = False
            try:
                result = await func(*args, **kwargs) 
            except Exception as err: 
                is_error = True
                result = ""
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

class MetricSummary(BaseModel):
    function_name: str
    avg_execution_time: float
    number_of_calls: int
    number_of_errors: int


class MetricsCollectionUseCase():
    async def get_metrics(self, function_name: str):
        with SessionManager() as db_session: 
            query_result = db_session.query(
                func.count(Metric.id).label("number_of_calls"),
                func.count(Metric.id).filter(Metric.is_error.is_(True)).label("number_of_errors"),
                func.avg(Metric.execution_time).label("avg_execution_time")
            ).filter(Metric.function_name==function_name).one_or_none()

            response = MetricSummary(
                function_name = function_name,
                avg_execution_time = query_result.avg_execution_time if query_result else 0,
                number_of_calls = query_result.number_of_calls if query_result else 0,
                number_of_errors = query_result.number_of_errors if query_result else 0
            )
        
        return response
