from tracdap.rt._impl.grpc.tracdap.config import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RuntimeConfig(_message.Message):
    __slots__ = ("config", "storage", "repositories", "sparkSettings")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class RepositoriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _common_pb2.PluginConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.PluginConfig, _Mapping]] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    SPARKSETTINGS_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    storage: _common_pb2.StorageConfig
    repositories: _containers.MessageMap[str, _common_pb2.PluginConfig]
    sparkSettings: SparkSettings
    def __init__(self, config: _Optional[_Mapping[str, str]] = ..., storage: _Optional[_Union[_common_pb2.StorageConfig, _Mapping]] = ..., repositories: _Optional[_Mapping[str, _common_pb2.PluginConfig]] = ..., sparkSettings: _Optional[_Union[SparkSettings, _Mapping]] = ...) -> None: ...

class SparkSettings(_message.Message):
    __slots__ = ("sparkProps",)
    class SparkPropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SPARKPROPS_FIELD_NUMBER: _ClassVar[int]
    sparkProps: _containers.ScalarMap[str, str]
    def __init__(self, sparkProps: _Optional[_Mapping[str, str]] = ...) -> None: ...
