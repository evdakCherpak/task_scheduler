from src.domain.exceptions import (
    InvalidDescriptionError,
    InvalidPayloadError,
    InvalidPriorityError,
    InvalidTaskTypeError,
)
from src.infra.logger import main_logger

PRIORITY_MIN = 1
PRIORITY_MAX = 10
STANDARD_PRIORITY = 7


class DescriptionDescriptor:
    def __set_name__(self, source_class, name):
        self.attr = f"_{name}"

    def __get__(self, obj, _objtype) -> str:
        if obj is None:
            return self  # type: ignore[return-value]
        return obj.__dict__[self.attr]

    def __set__(self, obj, value):
        if not isinstance(value, str) or not value.strip():
            main_logger.warning(f"DescriptionDescriptor: инвалидное значение {value}")
            raise InvalidDescriptionError(
                f"Описание задачи должно быть непустой строкой, получено: {value!r}"
            )
        obj.__dict__[self.attr] = value

class PriorityDescriptor:
    def __set_name__(self, source_class, name):
        self.attr = f"_{name}"

    def __get__(self, obj, _objtype) -> int:
        if obj is None:
            return self  # type: ignore[return-value]
        return obj.__dict__[self.attr]

    def __set__(self, obj, value):
        if not isinstance(value, int):
            main_logger.warning(f"PriorityDescriptor: инвалидный тип {type(value).__name__}")
            raise InvalidPriorityError(
                f"Приоритет должен быть целым числом, получено: {type(value).__name__}"
            )
        if not (PRIORITY_MIN <= value <= PRIORITY_MAX):
            main_logger.warning(f"PriorityDescriptor: значение вне диапозона [{PRIORITY_MIN, PRIORITY_MAX}]")
            raise InvalidPriorityError(
                f"Приоритет должен быть от {PRIORITY_MIN} до {PRIORITY_MAX}, получено: {value}"
            )
        obj.__dict__[self.attr] = value


class TaskTypeDescriptor:
    def __set_name__(self, source_class, name):
        self.attr = f"_{name}"

    def __get__(self, obj, _objtype) -> str:
        if obj is None:
            return self  # type: ignore[return-value]
        return obj.__dict__[self.attr]

    def __set__(self, obj, value):
        if not isinstance(value, str) or not value.strip():
            main_logger.warning(f"TaskTypeDescriptor: инвалидное значение {value}")
            raise InvalidTaskTypeError(
                f"Тип задачи должен быть непустой строкой, получено: {value!r}"
            )
        obj.__dict__[self.attr] = value

class PayloadDescriptor:
    def __set_name__(self, source_class, name):
        self.attr = f"_{name}"

    def __get__(self, obj, _objtype):
        if obj is None:
            return self  # type: ignore[return-value]
        return obj.__dict__[self.attr]

    def __set__(self, obj, value):
        if not isinstance(value, dict):
            main_logger.warning(f"PayloadDescriptor: инвалидный тип {type(value).__name__}")
            raise InvalidPayloadError(
                f"Payload задачи должен быть словарём, получено: {type(value).__name__}"
            )
        obj.__dict__[self.attr] = value
