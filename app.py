from handlers.email_handler import EmailHandler
from handlers.registry import HandlerRegistry
from manager.job_manager import JobManager
from queueing.job_queue import JobQueue
from workers.worker import Worker


def main() -> None:
    handler_registry = HandlerRegistry()

    # register handlers across job_types
    handler_registry.register("send_email", EmailHandler())

    queue = JobQueue()
    manager = JobManager(queue)

    # add jobs to queue
    manager.submit_job(
        job_type="send_email",
        payload={"to": "abc@xyz.com", "subject": "job1", "body": "job1"},
    )

    manager.submit_job(
        job_type="send_email",
        payload={"to": "def@xyz.com", "subject": "job2", "body": "job2"},
    )

    worker = Worker(manager, queue, handler_registry)
    worker.run()


if __name__ == "__main__":
    main()
