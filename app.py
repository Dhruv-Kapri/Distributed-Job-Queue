import threading

from handlers.email_handler import EmailHandler
from handlers.registry import HandlerRegistry
from manager.job_manager import JobManager
from models.job import JobStatus
from queueing.job_queue import JobQueue
from stores import SQLiteJobStore
from workers.worker import Worker


def main() -> None:
    handler_registry = HandlerRegistry()

    # register handlers across job_types
    handler_registry.register("send_email", EmailHandler())

    queue = JobQueue()
    job_store = SQLiteJobStore()
    manager = JobManager(queue, job_store)

    for job in job_store.list_by_status(JobStatus.QUEUED):
        queue.enqueue(job)

    worker_count: int = 3
    workers = [Worker(manager, queue, handler_registry) for _ in range(worker_count)]
    threads = [threading.Thread(target=worker.run) for worker in workers]

    for thread in threads:
        thread.start()

    # add jobs to queue
    test_jobs: int = 20
    for i in range(test_jobs):
        manager.submit_job(
            job_type="send_email",
            payload={"to": "abc@xyz.com", "subject": f"job{i}", "body": f"job{i}"},
        )

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
