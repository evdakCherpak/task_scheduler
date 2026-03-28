import uuid
from datetime import datetime, timezone
from src.domain.task import Task
from typing import TypedDict
from src.domain.exceptions import TaskCreateError


class RawData(TypedDict):
    task_type: str
    payload: dict
    priority: int



class TaskFactory:
    def __init__(self, source_name: str = "noname"):
        self.source = source_name

    def create(self, src_data: RawData) -> Task:
        task_type = src_data.get("task_type")
        if not task_type:
            raise TaskCreateError(f"Поле task_type - обязательное")
        return Task(
            id=str(uuid.uuid4()),
            task_type=task_type,
            payload=src_data.get("payload", {}),
            priority=src_data.get("priority", 5),
            created_at=datetime.now(timezone.utc)
        )
