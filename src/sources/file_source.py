import json
from uuid import UUID
from typing import Iterator, Any
from src.models.task import Task
from src.utils.logger import main_logger

def _parse_json_line_file(line: str, path: str, line_number: int) -> dict[str, Any]:
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError(f"Ошибка в файле {path}:{line_number}: {error}") from error

class FileTaskSource:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def put_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"FileTaskSource: открывание файла {self.filepath}")

        with open(self.filepath, encoding="utf-8") as fake_file:
            for line_num, line in enumerate(fake_file, start=1):
                line = line.strip()
                if not line:
                    continue
                data = _parse_json_line_file(line, self.filepath, line_num)
                yield Task(id=UUID(data["id"]), payload=data["payload"])


