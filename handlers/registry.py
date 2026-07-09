from handlers.base_handler import Handler


class HandlerRegistry:
    def __init__(self) -> None:
        self.handler_register: dict[str, Handler] = {}

    def register(self, job_type: str, handler: Handler) -> None:
        if not isinstance(job_type, str):
            raise TypeError("Job type has to be of type string")
        if not job_type:
            raise ValueError("Job type cannot be empty")

        if not isinstance(handler, Handler):
            raise TypeError("Handler has to be of type string")
        if not handler:
            raise ValueError("Handler cannot be null")

        self.handler_register[job_type] = handler

    def get(self, job_type: str) -> Handler | None:
        if not isinstance(job_type, str):
            raise TypeError("Job type has to be of type string")
        if not job_type:
            raise ValueError("Job type cannot be empty")

        return self.handler_register.get(job_type)
