from src.core.scheduler import Scheduler
from src.utils.logger import main_logger

class CLI:
    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    def run(self) -> None:
        try:
            tasks = list(self.scheduler.iter_tasks())
            for task in tasks:
                print(f"{task.id}: {task.payload}")
        except Exception as error:
            main_logger.error(f"Ошибка {error} при получении задач")
