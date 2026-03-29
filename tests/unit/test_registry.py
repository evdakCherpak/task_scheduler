import pytest
from src.app.sources.api_source import APITaskSource
from src.app.sources.file_source import FileTaskSource
from src.app.sources.gen_source import GenTaskSource


class TestSRCRegistry:
    def test_register_and_get(self, registry, json_file):
        registry.register("file", FileTaskSource)
        registry.register("api", APITaskSource)
        source = registry.get("file", filepath=json_file)
        assert isinstance(source, FileTaskSource)
        assert registry.get("api") is not None

    def test_get_unknown_raises_key_error(self, registry):
        with pytest.raises(KeyError, match="не найден"):
            registry.get("unknown")

    def test_contains(self, registry):
        registry.register("gen", GenTaskSource)
        assert "gen" in registry
        assert "missing" not in registry

    def test_iter_returns_source_names(self, registry):
        registry.register("a", APITaskSource)
        registry.register("b", GenTaskSource)
        names = list(registry)
        assert set(names) == {"a", "b"}

    def test_register_overwrite_warns(self, registry, caplog):
        registry.register("x", APITaskSource)
        registry.register("x", GenTaskSource)
        assert "перезаписан" in caplog.text

    def test_register_invalid_factory_raises(self, registry):
        class NotAProtocol:
            pass
        with pytest.raises(TypeError, match="не реализует TaskSourceProtocol"):
            registry.register("bad", NotAProtocol)
