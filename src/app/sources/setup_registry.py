from src.sources.registry import SRCRegistry
from src.sources.api_source import APITaskSource
from src.sources.file_source import FileTaskSource
from src.sources.gen_source import GenTaskSource
from src.utils.logger import main_logger

def registry_setup() -> SRCRegistry:
    main_logger.debug("Инициализация реестра источников задач")
    registry = SRCRegistry()
    registry.register("fake_api", APITaskSource)
    registry.register("file", FileTaskSource)
    registry.register("gen", GenTaskSource)
    main_logger.info("Реестр настроен: источники fake_api, file, gen")
    return registry
