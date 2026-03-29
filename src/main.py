from src.app.scheduler import Scheduler
from src.app.sources.registry import SRCRegistry
from src.app.sources.setup_registry import registry_setup
from src.delivery.cli import CLI
from src.infra.logger import main_logger


def main() -> None:
    main_logger.info("Запуск планировщика задач")
    registry: SRCRegistry = registry_setup()
    scheduler: Scheduler = Scheduler()

    main_logger.debug("Добавление источников задач")
    scheduler.add_source(registry.get("file", filepath="fake_data/tasks.json"))
    scheduler.add_source(registry.get(
        "gen",
        count=5,
        task_type="send_email",
        description="Отправить письмо пользователю",
        priority=5,
        payload={"to": "boltozviak@example.com"},
    ))
    scheduler.add_source(registry.get("fake_api"))

    cli: CLI = CLI(scheduler)
    cli.run()


if __name__ == "__main__":
    main()
