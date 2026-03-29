from typing import Iterator

from src.domain.task import Task
from src.infra.logger import main_logger


class APITaskSource:
    FAKE_DATA: dict = {
        "tasks": [
            {
                "task_type": "send_notification",
                "description": "Отправить push-уведомление пользователю",
                "priority": 6,
                "payload": {"user_id": 42, "message": "Ваш заказ обрабатывается"},
            },
            {
                "task_type": "recalc_stats",
                "description": "Пересчитать статистику за период",
                "priority": 4,
                "payload": {"period": "2024-Q1"},
            },
            {
                "task_type": "send_email",
                "description": "Отправить письмо пользователю",
                "priority": 8,
                "payload": {"to": "boltozviak@outlook.com", "subject": "Ваш отчёт готов"},
            },
        ]
    }

    def put_tasks(self) -> Iterator[Task]:
        main_logger.debug("APITaskSource: загрузка задач из API")
        for item in self.FAKE_DATA["tasks"]:
            yield Task.from_dict(item)
