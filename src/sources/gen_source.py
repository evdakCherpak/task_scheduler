import uuid
from typing import Iterator
from src.models.task import Task
from src.utils.logger import main_logger

class GenTaskSource:
    def __init__(self, count: int, task_message: str):
        if count < 1:
            raise ValueError("Число генерируемых задач должно быть >= 1")
        if not task_message.strip():
            raise ValueError("Сообщение в задаче не может быть пустым")
        self.count = count
        self.message = task_message

    def put_tasks(self) -> Iterator[Task]:
        main_logger.debug(f"Генерация {self.count} задач")
        
        for i in range(self.count):
            yield Task(id=uuid.uuid4(), payload={"message": self.message, "number": i})
