from typing import Callable, Iterator
from src.models.source_protocol import TaskSourceProtocol
from src.utils.logger import main_logger

SourceFactory = Callable[..., TaskSourceProtocol]

class SRCRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, SourceFactory] = {}

    def register(self, source: str, factory: SourceFactory) -> None:
        if not issubclass(factory, TaskSourceProtocol):
            raise TypeError(f"Источник '{source}':'{factory}' не реализует TaskSourceProtocol")
        if source in self._registry:
            main_logger.warning(f"Источник {source} перезаписан")
        self._registry[source] = factory
        main_logger.debug(f"Источник {source} внесен в реестр")

    def get(self, source: str, **kwargs):
        if source not in self._registry:
            raise KeyError(f"Источник {source} не найден")
        return self._registry[source](**kwargs)

    def __contains__(self, source: str):
        return source in self._registry
    
    def __iter__(self) -> Iterator[str]:
        return iter(self._registry)