from dataclasses import dataclass
from uuid import UUID
from typing import Any


@dataclass(frozen=True)
class Task:
    id: UUID
    payload: dict[str, Any]

