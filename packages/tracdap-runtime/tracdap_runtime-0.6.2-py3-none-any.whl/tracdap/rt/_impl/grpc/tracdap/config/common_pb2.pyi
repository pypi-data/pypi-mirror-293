from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class _ConfigFile(_message.Message):
    __slots__ = ("config",)
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    def __init__(self, config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PluginConfig(_message.Message):
    __slots__ = ("protocol", "properties", "secrets")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SecretsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    properties: _containers.ScalarMap[str, str]
    secrets: _containers.ScalarMap[str, str]
    def __init__(self, protocol: _Optional[str] = ..., properties: _Optional[_Mapping[str, str]] = ..., secrets: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PlatformInfo(_message.Message):
    __slots__ = ("environment", "production", "deploymentInfo")
    class DeploymentInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    PRODUCTION_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENTINFO_FIELD_NUMBER: _ClassVar[int]
    environment: str
    production: bool
    deploymentInfo: _containers.ScalarMap[str, str]
    def __init__(self, environment: _Optional[str] = ..., production: bool = ..., deploymentInfo: _Optional[_Mapping[str, str]] = ...) -> None: ...

class AuthenticationConfig(_message.Message):
    __slots__ = ("jwtIssuer", "jwtExpiry", "jwtLimit", "jwtRefresh", "provider", "disableAuth", "disableSigning", "systemUserId", "systemUserName", "systemTicketDuration", "systemTicketRefresh")
    JWTISSUER_FIELD_NUMBER: _ClassVar[int]
    JWTEXPIRY_FIELD_NUMBER: _ClassVar[int]
    JWTLIMIT_FIELD_NUMBER: _ClassVar[int]
    JWTREFRESH_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    DISABLEAUTH_FIELD_NUMBER: _ClassVar[int]
    DISABLESIGNING_FIELD_NUMBER: _ClassVar[int]
    SYSTEMUSERID_FIELD_NUMBER: _ClassVar[int]
    SYSTEMUSERNAME_FIELD_NUMBER: _ClassVar[int]
    SYSTEMTICKETDURATION_FIELD_NUMBER: _ClassVar[int]
    SYSTEMTICKETREFRESH_FIELD_NUMBER: _ClassVar[int]
    jwtIssuer: str
    jwtExpiry: int
    jwtLimit: int
    jwtRefresh: int
    provider: PluginConfig
    disableAuth: bool
    disableSigning: bool
    systemUserId: str
    systemUserName: str
    systemTicketDuration: int
    systemTicketRefresh: int
    def __init__(self, jwtIssuer: _Optional[str] = ..., jwtExpiry: _Optional[int] = ..., jwtLimit: _Optional[int] = ..., jwtRefresh: _Optional[int] = ..., provider: _Optional[_Union[PluginConfig, _Mapping]] = ..., disableAuth: bool = ..., disableSigning: bool = ..., systemUserId: _Optional[str] = ..., systemUserName: _Optional[str] = ..., systemTicketDuration: _Optional[int] = ..., systemTicketRefresh: _Optional[int] = ...) -> None: ...

class StorageConfig(_message.Message):
    __slots__ = ("buckets", "defaultBucket", "defaultFormat")
    class BucketsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PluginConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PluginConfig, _Mapping]] = ...) -> None: ...
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    DEFAULTBUCKET_FIELD_NUMBER: _ClassVar[int]
    DEFAULTFORMAT_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.MessageMap[str, PluginConfig]
    defaultBucket: str
    defaultFormat: str
    def __init__(self, buckets: _Optional[_Mapping[str, PluginConfig]] = ..., defaultBucket: _Optional[str] = ..., defaultFormat: _Optional[str] = ...) -> None: ...
