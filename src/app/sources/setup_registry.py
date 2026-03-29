from src.app.sources.registry import SRCRegistry
from src.app.sources.api_source import APITaskSource
from src.app.sources.file_source import FileTaskSource
from src.app.sources.gen_source import GenTaskSource
from src.infra.logger import main_logger

def registry_setup() -> SRCRegistry:
    main_logger.debug("Инициализация реестра источников задач")
    registry = SRCRegistry()
    registry.register("fake_api", APITaskSource)
    registry.register("file", FileTaskSource)
    registry.register("gen", GenTaskSource)
    main_logger.info("Реестр настроен: источники fake_api, file, gen")
    return registry
