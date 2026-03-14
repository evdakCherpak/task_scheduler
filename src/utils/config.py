import os
import datetime
from pathlib import Path

cur_date = datetime.datetime.now().date()
LOG_DIR = Path(__file__).resolve().parents[2]
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = LOG_DIR / f"scheduler-{cur_date}.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "mode": "a",
            "filename": str(LOG_FILE),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB before rotating
            "backupCount": 5,
            "level": "DEBUG",
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}