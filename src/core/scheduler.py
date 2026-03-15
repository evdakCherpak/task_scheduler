from src.models.task import Task
from src.models.source_protocol import TaskSourceProtocol
from src.utils.logger import main_logger
from collections.abc import Iterator, Sequence

class Scheduler:
    def __init__(self, sources: Sequence[TaskSourceProtocol] | None = None):
        self.sources = sources or []

    def add_source(self, source: TaskSourceProtocol) -> None:
        self.sources.append(source)
        main_logger.debug(f"Источник добавлен в планировщик: {type(source).__name__}")

    def iter_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"Начало итерации по задачам из {len(self.sources)} источников")
        for src in self.sources:
            if not isinstance(src, TaskSourceProtocol):
                main_logger.error(f"Источник {src} не соответствует TaskSourceProtocol")
                raise TypeError(f"Source {src} does not match TaskSourceProtocol")
            main_logger.debug(f"Загрузка задач из источника: {type(src).__name__}")
            for task in src.put_tasks():
                yield task
