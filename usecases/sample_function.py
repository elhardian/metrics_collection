import asyncio
from .metrics_collection import capture_execution

@capture_execution()
async def sleep_function(sleep_time: int = 10, raise_err: bool = False):
    if raise_err: raise Exception("ERROR")
    await asyncio.sleep(sleep_time)

@capture_execution()
async def sample_loop(length: int = 1000, raise_err: bool = False):
    if raise_err: raise Exception("ERROR")
    for i in range(0, length):
        await asyncio.sleep(0.001)

