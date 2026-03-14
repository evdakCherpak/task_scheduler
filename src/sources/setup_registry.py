from src.sources.registry import SRCRegistry
from src.sources.api_source import APITaskSource
from src.sources.file_source import FileTaskSource
from src.sources.gen_source import GenTaskSource

def registry_setup() -> SRCRegistry:
    registry = SRCRegistry()
    registry.register("fake_api", APITaskSource)
    registry.register("file", FileTaskSource)
    registry.register("gen", GenTaskSource)
    return registry
