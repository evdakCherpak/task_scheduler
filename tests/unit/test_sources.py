import pytest
from src.domain.task import Task
from src.domain.exceptions import InvalidTaskTypeError
from src.app.sources.file_source import FileTaskSource
from src.app.sources.gen_source import GenTaskSource


class TestFileTaskSource:
    def test_normal_call(self, json_file):
        source = FileTaskSource(filepath=json_file)
        tasks = list(source.put_tasks())
        assert len(tasks) == 2

    def test_task_type_and_payload_match_file(self, json_file):
        source = FileTaskSource(filepath=json_file)
        tasks = list(source.put_tasks())
        assert tasks[0].task_type == "cleanup"
        assert tasks[0].payload == {"path": "/tmp"}

    def test_nonexistent_file(self):
        source = FileTaskSource(filepath="tralala.json")
        with pytest.raises(FileNotFoundError):
            list(source.put_tasks())

    def test_retry_call_returns_same_task_types(self, json_file):
        source = FileTaskSource(filepath=json_file)
        first = [t.task_type for t in source.put_tasks()]
        second = [t.task_type for t in source.put_tasks()]
        assert first == second

    def test_all_tasks_are_task_instances(self, json_file):
        source = FileTaskSource(filepath=json_file)
        assert all(isinstance(t, Task) for t in source.put_tasks())


class TestGenTaskSource:
    def test_gen_correct_quantity(self, gen_source):
        tasks = list(gen_source.put_tasks())
        assert len(tasks) == 10

    def test_gen_all_unique_id(self, gen_source):
        ids = [task.id for task in gen_source.put_tasks()]
        assert len(set(ids)) == 10

    def test_gen_payload_contains_number(self, gen_source):
        tasks = list(gen_source.put_tasks())
        assert all("number" in task.payload for task in tasks)

    def test_gen_task_type_matches(self, gen_source):
        tasks = list(gen_source.put_tasks())
        assert all(task.task_type == "send_email" for task in tasks)

    def test_not_correct_count(self):
        with pytest.raises(ValueError):
            GenTaskSource(count=-1, task_type="email", description="desc", priority=5)

    def test_invalid_task_type_raises_on_generate(self):
        source = GenTaskSource(count=1, task_type="   ", description="desc", priority=5)
        with pytest.raises(InvalidTaskTypeError):
            list(source.put_tasks())

    def test_new_call_new_id(self):
        source = GenTaskSource(count=3, task_type="email", description="desc", priority=5)
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
        first = [task.task_type for task in api_source.put_tasks()]
        second = [task.task_type for task in api_source.put_tasks()]
        assert first == second
