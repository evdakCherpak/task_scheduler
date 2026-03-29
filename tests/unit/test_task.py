import pytest
from uuid import UUID
from src.domain.task import Task, TaskStatus
from src.domain.task_descriptors import PRIORITY_MIN, PRIORITY_MAX, STANDARD_PRIORITY
from src.domain.exceptions import (
    InvalidDescriptionError,
    InvalidPayloadError,
    InvalidPriorityError,
    InvalidStatusError,
    InvalidTaskTypeError,
)


def test_task_default_values():
    task = Task(task_type="send_email", description="Send report", priority=5)
    assert isinstance(task.id, UUID)
    assert task.task_type == "send_email"
    assert task.description == "Send report"
    assert task.priority == 5
    assert task.payload == {}
    assert task.status == TaskStatus.PENDING
    assert task.created_at is not None


def test_task_with_payload():
    task = Task(task_type="export", description="Export CSV", priority=3, payload={"format": "csv"})
    assert task.payload == {"format": "csv"}


def test_task_from_dict():
    data = {"task_type": "notify", "description": "Notify user", "priority": 4, "payload": {"uid": 1}}
    task = Task.from_dict(data)
    assert task.task_type == "notify"
    assert task.priority == 4
    assert task.payload == {"uid": 1}


def test_task_from_dict_defaults():
    data = {"task_type": "cleanup", "description": "Clean up temp files"}
    task = Task.from_dict(data)
    assert task.priority == STANDARD_PRIORITY
    assert task.payload == {}


def test_task_waiting_initially():
    task = Task(task_type="t", description="azaza", priority=5)
    assert task.task_waiting is True
    assert task.task_over is False


def test_task_over_done():
    task = Task(task_type="t", description="azaza", priority=5)
    task.status = TaskStatus.DONE
    assert task.task_over is True
    assert task.task_waiting is False


def test_task_over_failed():
    task = Task(task_type="t", description="azaza", priority=5)
    task.status = TaskStatus.FAILED
    assert task.task_over is True


def test_invalid_status_raises():
    task = Task(task_type="t", description="azaza", priority=5)
    with pytest.raises(InvalidStatusError):
        task.status = "done"


def test_invalid_task_type_empty():
    with pytest.raises(InvalidTaskTypeError):
        Task(task_type="", description="azaza", priority=5)


def test_invalid_task_type_whitespace():
    with pytest.raises(InvalidTaskTypeError):
        Task(task_type="   ", description="azaza", priority=5)


def test_invalid_task_type_non_string():
    with pytest.raises(InvalidTaskTypeError):
        Task(task_type=123, description="azaza", priority=5)


def test_invalid_description_empty():
    with pytest.raises(InvalidDescriptionError):
        Task(task_type="t", description="", priority=5)


def test_invalid_description_non_string():
    with pytest.raises(InvalidDescriptionError):
        Task(task_type="t", description=None, priority=5)


def test_priority_boundary_min():
    task = Task(task_type="t", description="azaza", priority=PRIORITY_MIN)
    assert task.priority == PRIORITY_MIN


def test_priority_boundary_max():
    task = Task(task_type="t", description="azaza", priority=PRIORITY_MAX)
    assert task.priority == PRIORITY_MAX


def test_priority_below_min_raises():
    with pytest.raises(InvalidPriorityError):
        Task(task_type="t", description="azaza", priority=PRIORITY_MIN - 1)


def test_priority_above_max_raises():
    with pytest.raises(InvalidPriorityError):
        Task(task_type="t", description="azaza", priority=PRIORITY_MAX + 1)


def test_priority_non_int_raises():
    with pytest.raises(InvalidPriorityError):
        Task(task_type="t", description="azaza", priority="high")


def test_invalid_payload_non_dict():
    with pytest.raises(InvalidPayloadError):
        Task(task_type="t", description="azaza", priority=5, payload=[1, 2, 3])


def test_invalid_payload_string():
    with pytest.raises(InvalidPayloadError):
        Task(task_type="t", description="azaza", priority=5, payload="data")
