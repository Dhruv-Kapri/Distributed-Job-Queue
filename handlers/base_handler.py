from abc import ABC, abstractmethod

from models.job import Job


class Handler(ABC):

    @abstractmethod
    def execute(self, job: Job) -> None:
        pass
