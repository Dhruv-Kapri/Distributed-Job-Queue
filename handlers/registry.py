class HandleRegistry:
    def __init__(self) -> None:
        self.handler_register: dict[str, str] = {}

    def register(self, job_type: str, handler: str) -> None:
        if not isinstance(job_type, str):
            raise TypeError("Job type has to be of type string")
        if not job_type:
            raise ValueError("Job type cannot be empty")
        
        if not isinstance(handler, str):
            raise TypeError("Handler has to be of type string")
        if not handler:
            raise ValueError("Handler cannot be null")

        self.handler_register[job_type] = handler

    def get(self, job_type: str) -> str:
        if not isinstance(job_type, str):
            raise TypeError("Job type has to be of type string")
        if not job_type:
            raise ValueError("Job type cannot be empty")

        handler = self.handler_register.get(job_type)

        if not handler:
            raise ValueError("Invalid job_type")
        
        return handler
