from typing import Protocol, runtime_checkable
from src.models.task import Task
from typing import Iterator


@runtime_checkable
class TaskSourceProtocol(Protocol):
    def put_tasks(self) -> Iterator[Task]:
        ...
