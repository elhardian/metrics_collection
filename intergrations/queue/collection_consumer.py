import asyncio
from helpers.logger import Logger
from pydantic import BaseModel, ValidationError
from intergrations.database import SessionManager
from models.metric import Metric

collection_queue = asyncio.Queue()

class MetricData(BaseModel):
    execution_time: float
    function_name: str

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
            except ValidationError as err:
                self.logger.error("Invalid metric data", err)
            except Exception as err:
                self.logger.error("Something went wrong during processing metric data", err)
            
    def insert_metric(self, metric_data: MetricData):
        with SessionManager() as db_session:
            metric = Metric(
                function_name = metric_data.function_name,
                execution_time = metric_data.execution_time
            )
            db_session.add(metric)
            db_session.commit()
            self.logger.debug("Metric saved to database")
