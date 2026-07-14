from queue import Queue

from models.job import Job


class JobQueue:
    def __init__(self) -> None:
        self._queue = Queue()

    def enqueue(self, job: Job) -> None:
        if job is None:
            raise ValueError("Job cannot be None")
        if not isinstance(job, Job):
            raise TypeError("Expected Job")

        self._queue.put(job)

    def dequeue(self) -> Job:
        return self._queue.get()

    def size(self) -> int:
        return self._queue.qsize()

    def is_empty(self) -> bool:
        return self._queue.empty()
