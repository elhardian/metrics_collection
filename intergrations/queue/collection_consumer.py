import asyncio
from helpers.logger import Logger
from pydantic import BaseModel, ValidationError
from intergrations.database import SessionManager
from models.metric import Metric
from typing import Optional

collection_queue = asyncio.Queue()

class MetricData(BaseModel):
    execution_time: float
    function_name: str
    is_error: Optional[bool] = False

class CollectionConsumer():
    def __init__(self, collection_queue: asyncio.Queue) -> None:
        self.queue = collection_queue
        self.logger = Logger(__name__)

    async def start(self):
        self.logger.info("Metrics collection consumer started, waiting for new message ...")
        while True:
            try:
                metric_data = await self.queue.get()
                self.logger.debug(f"Metric data received {metric_data}")
                
                metric_data = MetricData(**metric_data)
                self.insert_metric(metric_data)

                await self.summarize(metric_data.function_name)
            except ValidationError as err:
                self.logger.error("Invalid metric data", err)
            except Exception as err:
                self.logger.error("Something went wrong during processing metric data", err)
            
    def insert_metric(self, metric_data: MetricData):
        with SessionManager() as db_session:
            metric = Metric(
                function_name = metric_data.function_name,
                execution_time = metric_data.execution_time,
                is_error = metric_data.is_error
            )
            db_session.add(metric)
            db_session.commit()
            self.logger.debug("Metric saved to database")

    async def summarize(self, function_name: str):
        from usecases.metrics_collection import MetricsCollectionUseCase

        summary = await MetricsCollectionUseCase().get_metrics(function_name)
        self.logger.info(f"""
                        - Function                  : {summary.function_name}
                        - Number of calls           : {summary.number_of_calls}
                        - Number of errors          : {summary.number_of_errors}
                        - Average Execution Time    : {summary.avg_execution_time}
        """)
