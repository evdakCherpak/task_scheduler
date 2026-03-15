import pytest
from uuid import UUID
from src.models.source_protocol import TaskSourceProtocol
from src.models.task import Task
from src.sources.api_source import APITaskSource
from src.sources.file_source import FileTaskSource
from src.sources.gen_source import GenTaskSource

class WithoutPutTasks:
    ...

class WithPutTasks:
    def put_tasks(self):
        yield Task(id=UUID("00000000-0000-0000-0000-000000001111"), payload={})

class TestProtocolIsinctance:   
    def test_file_source_approve_protocol(self, file_source):
        assert isinstance(file_source, TaskSourceProtocol)

    def test_api_source_approve_protocol(self, api_source):
        assert isinstance(api_source, TaskSourceProtocol)
    
    def test_gen_source_approve_protocol(self, gen_source):
        assert isinstance(gen_source, TaskSourceProtocol)

    def test_random_source_not_approve_protocol(self):
        assert not isinstance(WithoutPutTasks(), TaskSourceProtocol)

    def test_random_source_approve_protocol(self):
        assert isinstance(WithPutTasks(), TaskSourceProtocol)

    
class TestProtocolSubclass:
    def test_file_source_class_approve_protocol(self):
        assert issubclass(FileTaskSource, TaskSourceProtocol)

    def test_api_source_class_approve_protocol(self):
        assert issubclass(APITaskSource, TaskSourceProtocol)

    def test_gen_source_class_approve_protocol(self):
        assert issubclass(GenTaskSource, TaskSourceProtocol)

    def test_random_class_not_approve_protocol(self):
        assert not issubclass(WithoutPutTasks, TaskSourceProtocol)

    def source_do_not_have_inheritance(self):
        assert not issubclass(FileTaskSource, GenTaskSource)
        assert not issubclass(FileTaskSource, APITaskSource)
        assert not issubclass(APITaskSource, GenTaskSource)
