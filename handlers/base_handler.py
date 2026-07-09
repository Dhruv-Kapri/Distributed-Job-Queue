from abc import ABC, abstractmethod

from models.job import Job


class Handler(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, job: Job) -> None:
        pass
