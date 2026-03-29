import pytest
from src.app.scheduler import Scheduler
from src.domain.task import Task


class WithoutPutTasks:
    ...


class TestScheduler:
    def test_add_source_and_iter_tasks(self, api_source):
        scheduler = Scheduler()
        scheduler.add_source(api_source)
        tasks = list(scheduler.iter_tasks())
        assert len(tasks) == 3
        assert all(isinstance(t, Task) for t in tasks)

    def test_iter_tasks_from_multiple_sources(self, api_source, gen_source):
        scheduler = Scheduler()
        scheduler.add_source(api_source)
        scheduler.add_source(gen_source)
        tasks = list(scheduler.iter_tasks())
        assert len(tasks) == 3 + 10

    def test_iter_tasks_invalid_source_raises(self):
        scheduler = Scheduler()
        scheduler.add_source(WithoutPutTasks())
        with pytest.raises(AttributeError):
            list(scheduler.iter_tasks())

    def test_init_with_sources(self, api_source):
        scheduler = Scheduler(sources=[api_source])
        tasks = list(scheduler.iter_tasks())
        assert len(tasks) == 3

    def test_init_with_none_sources(self):
        scheduler = Scheduler(sources=None)
        assert list(scheduler.iter_tasks()) == []
