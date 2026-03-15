import pytest
import json
from uuid import UUID
from src.models.task import Task
from src.sources.api_source import APITaskSource
from src.sources.file_source import FileTaskSource
from src.sources.gen_source import GenTaskSource
from src.sources.registry import SRCRegistry

@pytest.fixture
def task() -> Task:
    return Task(id=UUID("00000000-0000-0000-0000-000000000052"), payload={"message": "send_email", "for_who": "boltozviak@outlook.com"})

@pytest.fixture
def tasks() -> list[Task]:
    return [
        Task(id=UUID("00000000-0000-0000-0000-000000000052"), payload={"message": "send_email", "for_who": "boltozviak@outlook.com"}),
        Task(id=UUID("00000000-0000-0000-0000-000000000104"), payload={"message": "kek"}),
        Task(id=UUID("00000000-0000-0000-0000-000000000208"), payload={"message": "azaza"})
    ]

@pytest.fixture
def json_file(tmp_path) -> str:
    """JSONL: одна строка — один JSON с полями id, payload."""
    lines = [
        json.dumps({"id": "00000000-0000-0000-0000-000000000208", "payload": {"message": "azaza"}}),
        json.dumps({"id": "00000000-0000-0000-0000-000000000416", "payload": {"message": "kek"}}),
    ]
    path = tmp_path / "tasks.json"
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)

@pytest.fixture
def json_file_with_invalid_json(tmp_path) -> str:
    """Файл с невалидной JSON-строкой для теста ошибки парсинга."""
    path = tmp_path / "tasks.json"
    path.write_text('{"id": "00000000-0000-0000-0000-000000000001", "payload": {}}\n{ invalid }\n', encoding="utf-8")
    return str(path)



@pytest.fixture
def gen_source() -> GenTaskSource:
    return GenTaskSource(count=10, task_message="send_email")

@pytest.fixture
def file_source(json_file) -> FileTaskSource:
    return FileTaskSource(filepath=json_file)

@pytest.fixture
def api_source() -> APITaskSource:
    return APITaskSource()

@pytest.fixture
def registry() -> SRCRegistry:
    return SRCRegistry()

@pytest.fixture
def registry_with_sources(json_file) -> SRCRegistry:
    reg = SRCRegistry()
    reg.register("gen", GenTaskSource)
    reg.register("file", FileTaskSource)
    reg.register("fake_api", APITaskSource)
    return reg
    