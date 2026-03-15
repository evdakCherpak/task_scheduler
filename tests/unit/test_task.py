import uuid
from uuid import UUID
from src.models.task import Task


def test_creation_normal_task():
    task_id = uuid.uuid4()
    payload = {"message": "azaza"}
    task = Task(id=task_id, payload=payload)
    assert task.id == task_id
    assert task.payload == payload


def test_creation_empty_payload():
    task_id = uuid.uuid4()
    task = Task(id=task_id, payload={})
    assert task.id == task_id
    assert task.payload == {}


def test_two_similar_tasks():
    payload = {"message": "azaza"}
    uid = UUID("00000000-0000-0000-0000-000000000100")
    task1 = Task(id=uid, payload=payload)
    task2 = Task(id=uid, payload=payload)
    assert task1 == task2


def test_two_different_tasks():
    task1 = Task(id=UUID("00000000-0000-0000-0000-000000000100"), payload={})
    task2 = Task(id=UUID("00000000-0000-0000-0000-000000000101"), payload={})
    assert task1 != task2
