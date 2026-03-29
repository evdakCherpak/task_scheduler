import json
from typing import Any, Iterator

from src.domain.task import Task
from src.infra.logger import main_logger


def _parse_json_line(line: str, path: str, line_number: int) -> dict[str, Any]:
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        main_logger.warning(f"Ошибка парсинга JSON в {path}:{line_number}: {error}")
        raise ValueError(f"Ошибка в файле {path}:{line_number}: {error}") from error


class FileTaskSource:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def put_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"FileTaskSource: открытие файла {self.filepath}")
        count = 0
        with open(self.filepath, encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                data = _parse_json_line(line, self.filepath, line_num)
                yield Task.from_dict(data)
                count += 1
        main_logger.debug(f"FileTaskSource: загружено {count} задач из {self.filepath}")
