from models.job import Job
from stores.base_job_store import BaseJobStore


class InMemoryJobStore(BaseJobStore):
    """In-memory job store implementation."""

    def __init__(self):
        self.job_store = {}

    def add_job(self, job: Job) -> None:
        if job is not None and job.id is not None:
            self.job_store[job.id] = job

    def get_job(self, job_id) -> Job | None:
        if job_id is None:
            return None
        return self.job_store.get(job_id)

    def update_job(self, job_id, job: Job) -> None:
        if job_id is not None and job is not None and job_id in self.job_store:
            self.job_store[job_id] = job

    def delete_job(self, job_id) -> None:
        if job_id is not None and job_id in self.job_store:
            del self.job_store[job_id]
