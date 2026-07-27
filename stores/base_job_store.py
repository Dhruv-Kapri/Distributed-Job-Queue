from abc import ABC, abstractmethod

from models.job import Job


class BaseJobStore(ABC):
    @abstractmethod
    def add_job(self, job: Job) -> None:
        pass

    @abstractmethod
    def get_job(self, job_id) -> Job | None:
        pass

    @abstractmethod
    def update_job(self, job_id, job: Job) -> None:
        pass

    @abstractmethod
    def delete_job(self, job_id) -> None:
        pass
