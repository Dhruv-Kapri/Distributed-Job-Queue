from models.job import Job, JobStatus
from queueing.job_queue import JobQueue
from uuid import uuid4
from datetime import datetime


class JobManager:
    def __init__(self, queue: JobQueue) -> None:
        self.queue = queue
        self.job_store: dict[str, Job] = {}

    def submit_job(self, job_type: str, payload: dict) -> str:
        if not isinstance(job_type, str):
            raise TypeError("Type can only be of type string")
        if not job_type:
            raise ValueError("Type cannot be blank")

        if not isinstance(payload, dict):
            raise TypeError("Payload should be a dictionary")

        job_id = str(uuid4())
        now = datetime.now()
        new_job = Job(
            id=job_id,
            job_type=job_type,
            payload=payload,
            status=JobStatus.QUEUED,
            created_at=now,
            updated_at=now,
        )

        self.job_store[job_id] = new_job
        self.queue.enqueue(new_job)

        return job_id

    def get_job(self, job_id: str) -> Job | None:
        if not isinstance(job_id, str):
            raise TypeError("Type can only be of type string")
        if not job_id:
            raise ValueError("Empty job id is invalid")

        return self.job_store.get(job_id)

    def _update_status(self, job_id: str, status: JobStatus) -> None:
        if not isinstance(job_id, str):
            raise TypeError("Type can only be of type string")
        if not job_id:
            raise ValueError("Empty job id is invalid")

        job = self.job_store.get(job_id)

        if job is None:
            return

        job.status = status
        job.updated_at = datetime.now()

    def mark_running(self, job_id: str) -> None:
        self._update_status(job_id, JobStatus.RUNNING)

    def mark_completed(self, job_id: str) -> None:
        self._update_status(job_id, JobStatus.COMPLETED)

    def mark_failed(self, job_id: str) -> None:
        self._update_status(job_id, JobStatus.FAILED)
