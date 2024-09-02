from tracdap.rt._impl.grpc.tracdap.metadata import common_pb2 as _common_pb2
from tracdap.rt._impl.grpc.tracdap.config import common_pb2 as _common_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoutingProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PROTOCOL_NOT_SET: _ClassVar[RoutingProtocol]
    HTTP: _ClassVar[RoutingProtocol]
    GRPC: _ClassVar[RoutingProtocol]
    GRPC_WEB: _ClassVar[RoutingProtocol]
    REST: _ClassVar[RoutingProtocol]

class DeploymentLayout(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LAYOUT_NOT_SET: _ClassVar[DeploymentLayout]
    SANDBOX: _ClassVar[DeploymentLayout]
    HOSTED: _ClassVar[DeploymentLayout]
    CUSTOM: _ClassVar[DeploymentLayout]
PROTOCOL_NOT_SET: RoutingProtocol
HTTP: RoutingProtocol
GRPC: RoutingProtocol
GRPC_WEB: RoutingProtocol
REST: RoutingProtocol
LAYOUT_NOT_SET: DeploymentLayout
SANDBOX: DeploymentLayout
HOSTED: DeploymentLayout
CUSTOM: DeploymentLayout

class PlatformConfig(_message.Message):
    __slots__ = ("config", "platformInfo", "authentication", "metadata", "storage", "repositories", "executor", "jobCache", "tenants", "webServer", "gateway", "services", "deployment")
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
        value: _common_pb2_1.PluginConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_common_pb2_1.PluginConfig, _Mapping]] = ...) -> None: ...
    class TenantsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TenantConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TenantConfig, _Mapping]] = ...) -> None: ...
    class ServicesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ServiceConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ServiceConfig, _Mapping]] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    PLATFORMINFO_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    EXECUTOR_FIELD_NUMBER: _ClassVar[int]
    JOBCACHE_FIELD_NUMBER: _ClassVar[int]
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    WEBSERVER_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    platformInfo: _common_pb2_1.PlatformInfo
    authentication: _common_pb2_1.AuthenticationConfig
    metadata: MetadataConfig
    storage: _common_pb2_1.StorageConfig
    repositories: _containers.MessageMap[str, _common_pb2_1.PluginConfig]
    executor: _common_pb2_1.PluginConfig
    jobCache: _common_pb2_1.PluginConfig
    tenants: _containers.MessageMap[str, TenantConfig]
    webServer: WebServerConfig
    gateway: GatewayConfig
    services: _containers.MessageMap[str, ServiceConfig]
    deployment: DeploymentConfig
    def __init__(self, config: _Optional[_Mapping[str, str]] = ..., platformInfo: _Optional[_Union[_common_pb2_1.PlatformInfo, _Mapping]] = ..., authentication: _Optional[_Union[_common_pb2_1.AuthenticationConfig, _Mapping]] = ..., metadata: _Optional[_Union[MetadataConfig, _Mapping]] = ..., storage: _Optional[_Union[_common_pb2_1.StorageConfig, _Mapping]] = ..., repositories: _Optional[_Mapping[str, _common_pb2_1.PluginConfig]] = ..., executor: _Optional[_Union[_common_pb2_1.PluginConfig, _Mapping]] = ..., jobCache: _Optional[_Union[_common_pb2_1.PluginConfig, _Mapping]] = ..., tenants: _Optional[_Mapping[str, TenantConfig]] = ..., webServer: _Optional[_Union[WebServerConfig, _Mapping]] = ..., gateway: _Optional[_Union[GatewayConfig, _Mapping]] = ..., services: _Optional[_Mapping[str, ServiceConfig]] = ..., deployment: _Optional[_Union[DeploymentConfig, _Mapping]] = ...) -> None: ...

class MetadataConfig(_message.Message):
    __slots__ = ("database", "format")
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    database: _common_pb2_1.PluginConfig
    format: _common_pb2.MetadataFormat
    def __init__(self, database: _Optional[_Union[_common_pb2_1.PluginConfig, _Mapping]] = ..., format: _Optional[_Union[_common_pb2.MetadataFormat, str]] = ...) -> None: ...

class TenantConfig(_message.Message):
    __slots__ = ("defaultBucket", "defaultFormat")
    DEFAULTBUCKET_FIELD_NUMBER: _ClassVar[int]
    DEFAULTFORMAT_FIELD_NUMBER: _ClassVar[int]
    defaultBucket: str
    defaultFormat: str
    def __init__(self, defaultBucket: _Optional[str] = ..., defaultFormat: _Optional[str] = ...) -> None: ...

class WebServerConfig(_message.Message):
    __slots__ = ("enabled", "contentRoot", "rewriteRules", "redirects")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONTENTROOT_FIELD_NUMBER: _ClassVar[int]
    REWRITERULES_FIELD_NUMBER: _ClassVar[int]
    REDIRECTS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    contentRoot: _common_pb2_1.PluginConfig
    rewriteRules: _containers.RepeatedCompositeFieldContainer[WebServerRewriteRule]
    redirects: _containers.RepeatedCompositeFieldContainer[WebServerRedirect]
    def __init__(self, enabled: bool = ..., contentRoot: _Optional[_Union[_common_pb2_1.PluginConfig, _Mapping]] = ..., rewriteRules: _Optional[_Iterable[_Union[WebServerRewriteRule, _Mapping]]] = ..., redirects: _Optional[_Iterable[_Union[WebServerRedirect, _Mapping]]] = ...) -> None: ...

class WebServerRewriteRule(_message.Message):
    __slots__ = ("source", "target")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    source: str
    target: str
    def __init__(self, source: _Optional[str] = ..., target: _Optional[str] = ...) -> None: ...

class WebServerRedirect(_message.Message):
    __slots__ = ("source", "target", "status")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    source: str
    target: str
    status: int
    def __init__(self, source: _Optional[str] = ..., target: _Optional[str] = ..., status: _Optional[int] = ...) -> None: ...

class GatewayConfig(_message.Message):
    __slots__ = ("idleTimeout", "routes", "redirects")
    IDLETIMEOUT_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    REDIRECTS_FIELD_NUMBER: _ClassVar[int]
    idleTimeout: int
    routes: _containers.RepeatedCompositeFieldContainer[RouteConfig]
    redirects: _containers.RepeatedCompositeFieldContainer[WebServerRedirect]
    def __init__(self, idleTimeout: _Optional[int] = ..., routes: _Optional[_Iterable[_Union[RouteConfig, _Mapping]]] = ..., redirects: _Optional[_Iterable[_Union[WebServerRedirect, _Mapping]]] = ...) -> None: ...

class RouteConfig(_message.Message):
    __slots__ = ("routeName", "routeType", "protocols", "match", "target")
    ROUTENAME_FIELD_NUMBER: _ClassVar[int]
    ROUTETYPE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    routeName: str
    routeType: RoutingProtocol
    protocols: _containers.RepeatedScalarFieldContainer[RoutingProtocol]
    match: RoutingMatch
    target: RoutingTarget
    def __init__(self, routeName: _Optional[str] = ..., routeType: _Optional[_Union[RoutingProtocol, str]] = ..., protocols: _Optional[_Iterable[_Union[RoutingProtocol, str]]] = ..., match: _Optional[_Union[RoutingMatch, _Mapping]] = ..., target: _Optional[_Union[RoutingTarget, _Mapping]] = ...) -> None: ...

class RoutingMatch(_message.Message):
    __slots__ = ("host", "path")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    host: str
    path: str
    def __init__(self, host: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class RoutingTarget(_message.Message):
    __slots__ = ("scheme", "host", "port", "path")
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    scheme: str
    host: str
    port: int
    path: str
    def __init__(self, scheme: _Optional[str] = ..., host: _Optional[str] = ..., port: _Optional[int] = ..., path: _Optional[str] = ...) -> None: ...

class ServiceConfig(_message.Message):
    __slots__ = ("enabled", "alias", "port")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    alias: str
    port: int
    def __init__(self, enabled: bool = ..., alias: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class DeploymentConfig(_message.Message):
    __slots__ = ("layout",)
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    layout: DeploymentLayout
    def __init__(self, layout: _Optional[_Union[DeploymentLayout, str]] = ...) -> None: ...
