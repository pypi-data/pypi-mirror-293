import sys

from redis55 import asyncio  # noqa
from redis55.backoff import default_backoff
from redis55.client import Redis, StrictRedis
from redis55.cluster import RedisCluster
from redis55.connection import (
    BlockingConnectionPool,
    Connection,
    ConnectionPool,
    SSLConnection,
    UnixDomainSocketConnection,
)
from redis55.credentials import CredentialProvider, UsernamePasswordCredentialProvider
from redis55.exceptions import (
    AuthenticationError,
    AuthenticationWrongNumberOfArgsError,
    BusyLoadingError,
    ChildDeadlockedError,
    ConnectionError,
    DataError,
    InvalidResponse,
    OutOfMemoryError,
    PubSubError,
    ReadOnlyError,
    RedisError,
    ResponseError,
    TimeoutError,
    WatchError,
)
from redis55.sentinel import (
    Sentinel,
    SentinelConnectionPool,
    SentinelManagedConnection,
    SentinelManagedSSLConnection,
)
from redis55.utils import from_url

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


try:
    __version__ = metadata.version("redis55")
except metadata.PackageNotFoundError:
    __version__ = "99.99.99"


try:
    VERSION = tuple(map(int_or_str, __version__.split(".")))
except AttributeError:
    VERSION = tuple([99, 99, 99])

__all__ = [
    "AuthenticationError",
    "AuthenticationWrongNumberOfArgsError",
    "BlockingConnectionPool",
    "BusyLoadingError",
    "ChildDeadlockedError",
    "Connection",
    "ConnectionError",
    "ConnectionPool",
    "CredentialProvider",
    "DataError",
    "from_url",
    "default_backoff",
    "InvalidResponse",
    "OutOfMemoryError",
    "PubSubError",
    "ReadOnlyError",
    "Redis",
    "RedisCluster",
    "RedisError",
    "ResponseError",
    "Sentinel",
    "SentinelConnectionPool",
    "SentinelManagedConnection",
    "SentinelManagedSSLConnection",
    "SSLConnection",
    "UsernamePasswordCredentialProvider",
    "StrictRedis",
    "TimeoutError",
    "UnixDomainSocketConnection",
    "WatchError",
]
