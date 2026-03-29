from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4
from src.domain.task_descriptors import STANDARD_PRIORITY

from src.domain.exceptions import InvalidStatusError
from src.domain.task_descriptors import (
    DescriptionDescriptor,
    PayloadDescriptor,
    PriorityDescriptor,
    TaskTypeDescriptor,
)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"

class Task:
    task_type = TaskTypeDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    payload = PayloadDescriptor()

    def __init__(
        self,
        task_type: str,
        description: str,
        priority: int,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self._id: UUID = uuid4()
        self.task_type = task_type
        self.description = description
        self.priority = priority if priority is not None else STANDARD_PRIORITY
        self.payload = payload if payload is not None else {}
        self._status: TaskStatus = TaskStatus.PENDING
        self._created_at: datetime = datetime.now(timezone.utc)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        if not isinstance(value, TaskStatus):
            raise InvalidStatusError("Задан некорректный статус")
        self._status = value


    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def task_waiting(self) -> bool:
        return self._status == TaskStatus.PENDING

    @property
    def task_over(self) -> bool:
        return self._status in (TaskStatus.DONE, TaskStatus.FAILED)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            task_type=str(data["task_type"]),
            description=str(data["description"]),
            priority=int(data["priority"]) if "priority" in data else STANDARD_PRIORITY,  # type: ignore[arg-type]
            payload=dict(data["payload"]) if "payload" in data else {},  # type: ignore[arg-type]
        )
