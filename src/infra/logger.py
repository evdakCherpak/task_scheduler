import logging
from logging.config import dictConfig
from src.infra.config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)
main_logger = logging.getLogger("scheduler")
