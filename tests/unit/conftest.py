import pytest
import json
from src.domain.task import Task
from src.app.sources.api_source import APITaskSource
from src.app.sources.file_source import FileTaskSource
from src.app.sources.gen_source import GenTaskSource
from src.app.sources.registry import SRCRegistry


@pytest.fixture
def task() -> Task:
    return Task(task_type="send_email", description="Send test email", priority=5)


@pytest.fixture
def tasks() -> list[Task]:
    return [
        Task(task_type="send_email", description="Send email to user", priority=5),
        Task(task_type="cleanup", description="Clean up temp files", priority=3),
        Task(task_type="notify", description="Send push notification", priority=7),
    ]


@pytest.fixture
def json_file(tmp_path) -> str:
    """JSONL: одна строка — один JSON с полями task_type, description, priority, payload."""
    lines = [
        json.dumps({"task_type": "cleanup", "description": "Clean temp files", "priority": 3, "payload": {"path": "/tmp"}}),
        json.dumps({"task_type": "notify", "description": "Send notification", "priority": 5, "payload": {"user_id": 1}}),
    ]
    path = tmp_path / "tasks.json"
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


@pytest.fixture
def json_file_with_invalid_json(tmp_path) -> str:
    """Файл с невалидной JSON-строкой для теста ошибки парсинга."""
    path = tmp_path / "tasks.json"
    path.write_text(
        '{"task_type": "cleanup", "description": "desc", "priority": 3}\n{ invalid }\n',
        encoding="utf-8",
    )
    return str(path)


@pytest.fixture
def gen_source() -> GenTaskSource:
    return GenTaskSource(count=10, task_type="send_email", description="Send email", priority=5)


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
