from abc import ABC, abstractmethod

from models.job import Job, JobStatus


class BaseJobStore(ABC):
    @abstractmethod
    def add_job(self, job: Job) -> None:
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Job | None:
        pass

    @abstractmethod
    def update_job(self, job_id: str, job: Job) -> None:
        pass

    @abstractmethod
    def delete_job(self, job_id: str) -> None:
        pass

    @abstractmethod
    def list_by_status(self, status: JobStatus) -> list[Job]:
        pass
