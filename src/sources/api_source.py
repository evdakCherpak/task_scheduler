from uuid import UUID
from typing import Iterator
from src.models.task import Task


class APITaskSource:
    FAKE_DATA: dict = {
        "tasks": [
            {"id": "00000000-0000-0000-0000-000000000004", "payload": {"type": "send_notification", "user_id": 42}},
            {"id": "00000000-0000-0000-0000-000000000005", "payload": {"type": "recalc_stats", "period": "2024-Q1"}},
            {"id": "00000000-0000-0000-0000-000000000006", "payload": {"type": "send_email", "to": "boltozviak@outlook.com"}},
        ]
    }

    def put_tasks(self) -> Iterator[Task]:
        data = self.FAKE_DATA

        for line in data["tasks"]:
            yield Task(id=UUID(line["id"]), payload=line["payload"])
