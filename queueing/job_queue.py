from collections import deque

from models.job import Job


class JobQueue:
    def __init__(self) -> None:
        self._queue = deque()

    def enqueue(self, job: Job) -> None:
        if job is None:
            raise ValueError("Job cannot be None")
        if not isinstance(job, Job):
            raise TypeError("Expected Job")

        self._queue.append(job)

    def dequeue(self) -> Job | None:
        if not self._queue:
            return None

        return self._queue.popleft()

    def size(self) -> int:
        return len(self._queue)

    def is_empty(self) -> bool:
        return len(self._queue) == 0
