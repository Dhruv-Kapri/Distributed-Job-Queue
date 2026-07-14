import threading
import time

from handlers.base_handler import Handler
from models.job import Job


class EmailHandler(Handler):
    def execute(self, job: Job) -> None:
        if not isinstance(job, Job):
            raise TypeError("Expected Job")
        if job is None:
            raise ValueError("Job cannot be None")

        print(f"{threading.current_thread().name} Starting {job.payload['subject']}")

        time.sleep(5)

        print(f"{threading.current_thread().name} Finished {job.payload['subject']}")
