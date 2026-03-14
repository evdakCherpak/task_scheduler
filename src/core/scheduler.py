from src.models.task import Task
from src.models.source_protocol import TaskSourceProtocol
from src.utils.logger import main_logger
from collections.abc import Iterator, Sequence

class Scheduler:
    def __init__(self, sources: Sequence[TaskSourceProtocol] | None = None):
        self.sources = sources or []

    def add_source(self, source: TaskSourceProtocol) -> None:
        self.sources.append(source)

    def iter_tasks(self) -> Iterator[Task]:
        for src in self.sources:
            if not isinstance(src, TaskSourceProtocol):
                raise TypeError(f"Source {src} does not match TaskSourceProtocol")
            for task in src.put_tasks():
                yield task
