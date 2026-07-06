from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class JobStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class Job:
    id: str
    type: str
    payload: dict
    status: JobStatus
    created_at: datetime
    updated_at: datetime
