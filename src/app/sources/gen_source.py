from typing import Any, Iterator

from src.domain.task import Task
from src.infra.logger import main_logger


class GenTaskSource:
    def __init__(
        self,
        count: int,
        task_type: str,
        description: str,
        priority: int,
        payload: dict[str, Any] | None = None,
    ) -> None:
        if count < 1:
            raise ValueError("Число генерируемых задач должно быть >= 1")
        self.count = count
        self.task_type = task_type
        self.description = description
        self.priority = priority
        self.payload = payload or {}

    def put_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"GenTaskSource: генерация {self.count} задач типа {self.task_type!r}")
        for i in range(self.count):
            yield Task(
                task_type=self.task_type,
                description=self.description,
                priority=self.priority,
                payload={**self.payload, "number": i},
            )
