import pytest
from uuid import UUID
from src.domain.task import Task
from src.app.sources.file_source import FileTaskSource
from src.app.sources.gen_source import GenTaskSource


class TestFileTaskSource:
    def test_normal_call(self, json_file):
        source= FileTaskSource(filepath=json_file)
        tasks = list(source.put_tasks())
        assert len(tasks) == 2

    def test_id_and_payload_same_like_in_file(self, json_file):
        source = FileTaskSource(filepath=json_file)
        tasks = list(source.put_tasks())
        assert tasks[0].id == UUID("00000000-0000-0000-0000-000000000208")
        assert tasks[0].payload == {"message": "azaza"}

    def test_nonexistent_file(self):
        source = FileTaskSource(filepath="tralala.json")
        with pytest.raises(FileNotFoundError):
            list(source.put_tasks())

    def test_retry_call_return_same_tasks(self, json_file):
        source = FileTaskSource(filepath=json_file)
        first = list(source.put_tasks())
        second = list(source.put_tasks())
        assert [task.id for task in first] == [task.id for task in second]



class TestGenTaskSource:
    def test_gen_correct_quantity(self, gen_source):
        tasks = list(gen_source.put_tasks())
        assert len(tasks) == 10

    def test_gen_all_unique_id(self, gen_source):
        ids = [task.id for task in gen_source.put_tasks()]
        assert len(set(ids)) == 10

    def test_gen_all_payloads_have_message(self, gen_source):
        tasks = list(gen_source.put_tasks())
        assert all(task.payload["message"] == "send_email" for task in tasks)

    def test_not_correct_count(self):
        with pytest.raises(ValueError):
            GenTaskSource(count=(-1), task_message="email")

    def test_empty_message(self):
        with pytest.raises(ValueError):
            GenTaskSource(count=3, task_message="   ")

    def test_new_call_new_id(self):
        source = GenTaskSource(count=3, task_message="email")
        first = [task.id for task in source.put_tasks()]
        second = [task.id for task in source.put_tasks()]
        assert first != second

class TestAPITaskSource:
    def test_normal_call(self, api_source):
        tasks = list(api_source.put_tasks())
        assert all(isinstance(task, Task) for task in tasks)

    def test_payload_not_empty(self, api_source):
        tasks = list(api_source.put_tasks())
        assert all(task.payload for task in tasks)

    def test_retry_call_return_same_data(self, api_source):
        first = [task.id for task in api_source.put_tasks()]
        second = [task.id for task in api_source.put_tasks()]
        assert first == second
