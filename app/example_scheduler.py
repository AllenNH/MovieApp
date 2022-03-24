import logging
import asyncio
from arq.worker import create_worker
from arq.connections import RedisSettings
from arq import cron

logger = logging.getLogger(__name__)

async def hello_world(ctx):
    job_id = ctx["job_id"]
    print(f"hello world ({job_id})")

class ArqWorkerSettings:
    functions = [hello_world]
    # TODO: Issue with unique cron jobs and multiple arq workers: https://github.com/samuelcolvin/arq/issues/196
    cron_jobs = [
        cron(hello_world, second=1, unique=True)
    ]
    redis_settings = RedisSettings()

class ArqWorker:
    def __init__(self):
        self.worker = None
        self.task = None

    async def start(self, **kwargs):
        self.worker = create_worker(ArqWorkerSettings, **kwargs)
        self.task = asyncio.create_task(self.worker.async_run())

    async def close(self):
        await self.worker.close()

arq_worker = ArqWorker()

print("Hello1")
