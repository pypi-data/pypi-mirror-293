from tracdap.rt._impl.grpc.tracdap.metadata import object_id_pb2 as _object_id_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import object_pb2 as _object_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import job_pb2 as _job_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobConfig(_message.Message):
    __slots__ = ("jobId", "job", "resources", "resourceMapping", "resultMapping")
    class ResourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _object_pb2.ObjectDefinition
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_object_pb2.ObjectDefinition, _Mapping]] = ...) -> None: ...
    class ResourceMappingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _object_id_pb2.TagHeader
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_object_id_pb2.TagHeader, _Mapping]] = ...) -> None: ...
    class ResultMappingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _object_id_pb2.TagHeader
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_object_id_pb2.TagHeader, _Mapping]] = ...) -> None: ...
    JOBID_FIELD_NUMBER: _ClassVar[int]
    JOB_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    RESOURCEMAPPING_FIELD_NUMBER: _ClassVar[int]
    RESULTMAPPING_FIELD_NUMBER: _ClassVar[int]
    jobId: _object_id_pb2.TagHeader
    job: _job_pb2.JobDefinition
    resources: _containers.MessageMap[str, _object_pb2.ObjectDefinition]
    resourceMapping: _containers.MessageMap[str, _object_id_pb2.TagHeader]
    resultMapping: _containers.MessageMap[str, _object_id_pb2.TagHeader]
    def __init__(self, jobId: _Optional[_Union[_object_id_pb2.TagHeader, _Mapping]] = ..., job: _Optional[_Union[_job_pb2.JobDefinition, _Mapping]] = ..., resources: _Optional[_Mapping[str, _object_pb2.ObjectDefinition]] = ..., resourceMapping: _Optional[_Mapping[str, _object_id_pb2.TagHeader]] = ..., resultMapping: _Optional[_Mapping[str, _object_id_pb2.TagHeader]] = ...) -> None: ...
