import time

from handlers.base_handler import Handler
from handlers.registry import HandlerRegistry
from manager.job_manager import JobManager
from models.job import Job
from queueing.job_queue import JobQueue


class Worker:
    def __init__(
        self,
        job_manager: JobManager,
        job_queue: JobQueue,
        handler_registry: HandlerRegistry,
    ) -> None:
        self.manager = job_manager
        self.queue = job_queue
        self.registry = handler_registry

    def run(self) -> None:
        while True:
            job: Job | None = self.queue.dequeue()
            if not job:
                time.sleep(1)
                continue

            handler: Handler | None = self.registry.get(job.job_type)
            if not handler:
                self.manager.mark_failed(job.id)
                continue

            self.manager.mark_running(job.id)

            try:
                handler.execute(job)
                self.manager.mark_completed(job.id)

            except Exception as e:
                print(f"Job not completed due to issue: {e}")
                self.manager.mark_failed(job.id)
