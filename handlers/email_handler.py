from handlers.base_handler import Handler
from models.job import Job


class EmailHandler(Handler):
    def execute(self, job: Job) -> None:
        if not isinstance(job, Job):
            raise TypeError("Expected Job")
        if job is None:
            raise ValueError("Job cannot be None")

        print(f"Sending email to {job.payload['to']}")
        return
