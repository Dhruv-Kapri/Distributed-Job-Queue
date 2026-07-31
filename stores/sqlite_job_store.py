import json
import sqlite3
import threading
from datetime import datetime

from models.job import Job, JobStatus

from .base_job_store import BaseJobStore


class SQLiteJobStore(BaseJobStore):
    def __init__(self, db_path: str = "jobs.db") -> None:
        # Initialize the SQLite database connection and create the jobs table if it doesn't exist
        self._conn = sqlite3.connect(
            db_path,
            check_same_thread=False,  # useful when multiple worker threads share the store
        )
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._create_jobs_table()

    def _create_jobs_table(self) -> None:
        # Create the jobs table if it doesn't exist
        with self._lock, self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    job_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
                """
            )

    def add_job(self, job: Job) -> None:
        # Add the job to the SQLite database
        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO jobs (id, job_type, payload, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.job_type,
                    json.dumps(
                        job.payload
                    ),  # Convert payload dict to string for storage
                    job.status.value,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                ),
            )

    def get_job(self, job_id) -> Job | None:
        # Retrieve the job from the SQLite database by job_id
        with self._lock, self._conn:
            cursor = self._conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            if row:
                return Job(
                    id=row["id"],
                    job_type=row["job_type"],
                    payload=json.loads(row["payload"]),  # Convert string back to dict
                    status=JobStatus(row["status"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )

    def update_job(self, job_id, job: Job) -> None:
        # Update the job in the SQLite database by job_id
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE jobs
                SET job_type = ?, payload = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    job.job_type,
                    json.dumps(job.payload),
                    job.status.value,
                    job.updated_at.isoformat(),
                    job_id,
                ),
            )

    def delete_job(self, job_id) -> None:
        # Delete the job from the SQLite database by job_id
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))

    def list_by_status(self, status: JobStatus) -> list[Job]:
        with self._lock, self._conn:
            cursor = self._conn.execute(
                "SELECT * FROM jobs WHERE status = ?", (status.value,)
            )
            jobs = []
            for row in cursor.fetchall():
                jobs.append(
                    Job(
                        id=row["id"],
                        job_type=row["job_type"],
                        payload=json.loads(row["payload"]),
                        status=JobStatus(row["status"]),
                        created_at=datetime.fromisoformat(row["created_at"]),
                        updated_at=datetime.fromisoformat(row["updated_at"]),
                    )
                )
            return jobs
