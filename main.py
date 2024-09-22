
import asyncio
from helpers.logger import Logger
from intergrations.queue.collection_consumer import CollectionConsumer, collection_queue
from intergrations.database import engine
from usecases.sample_function import sample_loop, sleep_function
from usecases.metrics_collection import MetricsCollectionUseCase
from models.base import Base

logger = Logger(__name__)

def initialize_database():
    Base.metadata.create_all(engine)

# Define the tasks here
tasks = [
    {
        "to_do": sleep_function,
        "kwargs": {"sleep_time": 10}
    },
    {
        "to_do": sleep_function,
        "kwargs": {"sleep_time": 20, "raise_err": True}
    },
    {
        "to_do": sample_loop,
        "kwargs": {"length": 1000, "raise_err": True}
    },
    {
        "to_do": sample_loop,
        "kwargs": {"length": 5000}
    },
]

async def main():
    logger.info("Initializing database ...")
    initialize_database()

    logger.info("Application started!")
    consumer = CollectionConsumer(collection_queue)
    asyncio.create_task(consumer.start())
    
    # RUN YOUR TASKS HERE
    for task in tasks:
        to_do = task.get("to_do")
        asyncio.create_task(to_do(**task.get("kwargs")))

    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application Closed")
    except Exception as err:
        logger.error("Application closed, something went wrong", err)