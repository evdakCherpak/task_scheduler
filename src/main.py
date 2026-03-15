from src.core.cli import CLI
from src.sources.registry import SRCRegistry
from src.sources.setup_registry import registry_setup   
from src.core.scheduler import Scheduler
from src.utils.logger import main_logger

def main() -> None:
    main_logger.info("Запуск планировщика задач")
    registry: SRCRegistry = registry_setup()
    scheduler: Scheduler = Scheduler()
    main_logger.debug("Добавление источников задач")
    scheduler.add_source(registry.get("file", filepath="fake_data/tasks.json"))
    scheduler.add_source(registry.get("gen", count=7, task_message="send_email"))
    scheduler.add_source(registry.get("fake_api"))

    cli: CLI = CLI(scheduler)
    cli.run()

if __name__ == "__main__":
    main()
