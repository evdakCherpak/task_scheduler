from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from src.domain.task import Task


@runtime_checkable
class TaskSourceProtocol(Protocol):
    def put_tasks(self) -> Iterator[Task]:
        ...
