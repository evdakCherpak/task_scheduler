from src.domain.task import Task
from src.domain.source_protocol import TaskSourceProtocol
from src.infra.logger import main_logger
from collections.abc import Iterator, Sequence

class Scheduler:
    def __init__(self, sources: Sequence[TaskSourceProtocol] | None = None):
        self.sources = list(sources) if sources else []

    def add_source(self, source: TaskSourceProtocol) -> None:
        self.sources.append(source)
        main_logger.debug(f"Источник добавлен в планировщик: {type(source).__name__}")

    def iter_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"Начало итерации по задачам из {len(self.sources)} источников")
        for src in self.sources:
            main_logger.debug(f"Загрузка задач из источника: {type(src).__name__}")
            for task in src.put_tasks():
                yield task
