# Task Scheduler

Пет-проект: планировщик задач с подключаемыми источниками и консольным выводом.

## Структура проекта

- **`src/models/`** — модель задачи (`Task`: id UUID, payload), протокол источника (`TaskSourceProtocol.put_tasks()`)
- **`src/core/`** — планировщик (`Scheduler`: добавление источников, итерация по задачам) и CLI (вывод списка задач в консоль)
- **`src/sources/`** — источники задач: файл в формате JSONL, генератор по количеству и сообщению, заглушка API; реестр фабрик (`SRCRegistry`) и настройка по умолчанию (`registry_setup`)
- **`src/utils/`** — конфиг логирования (папка `logs/` в корне проекта, ротация файлов) и общий логгер
- **`src/main.py`** — точка входа: поднимает реестр, вешает три источника на планировщик, запускает CLI

Расширение: новые источники реализуют `TaskSourceProtocol` и регистрируются в реестре; в `main` добавляются вызовы `scheduler.add_source(registry.get(...))`.

## Установка и запуск

```bash
pip install -r requirements.txt
#или
uv sync

python3 -m src.main
```

Ожидается файл `fake_data/tasks.json` в формате JSONL (одна строка — один JSON с полями `id` (UUID-строка) и `payload`).

## Тесты

```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=src
```

Тесты в `tests/unit/`: модель задачи, протокол, реестр, планировщик, источники (файл, генератор, API), CLI; фикстуры в `conftest.py`.

