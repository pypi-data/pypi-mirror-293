import os
import copy
import logging
from pprint import pformat
from pathlib import Path
from typing import Self, Any, Iterator
from enum import Enum

from .access import ClusterAccess


class WantKind(Enum):
    CFGMAP = 0
    SECRET = 1


class Wants:
    def __init__(self, kind, *paths):
        self.kind = kind
        self.paths = list(paths)
        self.suffix = ""
        self.logger = None
        self.converter = lambda x: x

    @classmethod
    def cfgmap(self, *paths):
        return Wants(WantKind.CFGMAP, *paths)

    @classmethod
    def secret(self, *paths):
        return Wants(WantKind.SECRET, *paths)

    def set_logger(self, logger):
        self.logger = logger

    def append(self, suffix) -> Self:
        self.suffix = suffix
        return self

    def to(self, converter) -> Self:
        self.converter = converter
        return self

    def to_int(self) -> Self:
        return self.to(int)

    def to_bool(self) -> Self:
        return self.to(
            lambda s: {
                "true": True,
                "1": True,
                "false": False,
                "0": False,
            }[s.lower()]
        )

    def __add__(self, other) -> Self:
        return self.append(other)

    def __repr__(self) -> str:
        prefix = self._get_prefix(cfgmap = "cfgmap", secret = "secret")
        args = ", ".join([str(path) for path in self.paths]) + self.suffix
        return f"Wants.{prefix}({args})"

    def _get_prefix(self, extra_prefix: str = "", cfgmap = "configmaps", secret = "secrets") -> str:
        if self.kind == WantKind.CFGMAP:
            return f"{extra_prefix}{cfgmap}"
        if self.kind == WantKind.SECRET:
            return f"{extra_prefix}{secret}"

    def _fill_paths(self, filler_func) -> Self:
        return [
            filler_func(path) if isinstance(path, self.__class__) else path
            for path in self.paths
        ]

    def _return(self, val):
        result = val
        if not self.suffix == "":
            try:
                result = result + self.suffix
            except Exception as e:
                self.logger.warning(f"Could not add suffix {self.suffix} to value {val}:\n{e}")

        try:
            return self.converter(result)
        except Exception as e:
            self.logger.warning(f"Could not convert {result} to desired type")
            return result

    def fill_from_store(self, access: ClusterAccess) -> Any:
        paths = self._fill_paths(lambda path: path.fill_from_store(access))
        if self.kind == WantKind.CFGMAP:
            return self._return(access.cfgmap(*paths))
        if self.kind == WantKind.SECRET:
            return self._return(access.secret(*paths))

    def fill_from_env(self) -> Self|str:
        paths = self._fill_paths(lambda path: path.fill_from_env())

        prefix = self._get_prefix().upper()
        env_var = "_".join([prefix] + [str(path).upper().replace("-", "_") for path in paths])

        try:
            return self._return(os.environ[env_var])
        except Exception as e:
            if self.logger is not None:
                self.logger.warning(f"Could not find environment variable {env_var}:\n{e}")
            return self

    def fill_from_dict(self, paths_dict: dict[str,str]) -> Self|str:
        paths = self._fill_paths(lambda path: path.fill_from_dict(paths_dict))

        self_path = Path(self._get_prefix("/")).joinpath(*paths)
        try:
            return self._return(paths_dict[self_path])
        except Exception as e:
            if self.logger is not None:
                self.logger.warning(f"Could not find {self_path} in arguments:\n{e}")
            return self


class Config:
    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)
        self._attrs = {
            Config(**val) if isinstance(val, dict) else val
            for key, val in kwargs.items()
        }
        self._attrs = {}
        for key, val in kwargs.items():
            if isinstance(val, dict):
                val = Config(**val)
            if isinstance(val, Config) or isinstance(val, Wants):
                val.set_logger(self._logger)

            self._attrs[key] = val

    @classmethod
    def from_dict(self, items: dict) -> Self:
        return Config(**items)

    def to_dict(self):
        return {
            key: val.to_dict() if isinstance(val, self.__class__) else val
            for key, val in self.items()
        }

    def extend(self, other: Self) -> Self:
        if isinstance(other, dict):
            other = Config.from_dir(other)
        self._attrs = self._attrs | other._attrs
        return self

    def __getattr__(self, key: str):
        if key[0] == "_":
            return super().__getattr__(key)
        return self._attrs[key]

    def __setattr__(self, key: str, val):
        if key[0] == "_":
            return super().__setattr__(key, val)
        self._attrs[key] = val

    def __getitem__(self, key: str):
        return self._attrs[key]

    def __setitem__(self, key: str, val):
        self._attrs[key] = val

    def __repr__(self) -> str:
        return pformat(self.to_dict())

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def set_logger(self, logger) -> Self:
        self._logger = logger
        return self

    def get_nested(self, keys: list[str]):
        head, tail = keys[0], keys[1:]
        if len(tail) == 0:
            return self[head]

        return self[head].get_nested(tail)

    def set_nested(self, keys: list[str], val):
        head, tail = keys[0], keys[1:]
        if len(tail) == 0:
            self[head] = val
        else:
            self[head].set_nested(tail, val)

    def _fill(self, filler_func) -> Self:
        for key, val in self.items():
            if isinstance(val, self.__class__) or isinstance(val, Wants):
                self[key] = filler_func(val)
        return self

    def fill_from_store(self, access: ClusterAccess|None = None) -> Self:
        if access is None:
            access = ClusterAccess()
        return self._fill(lambda val: val.fill_from_store(access))

    def fill_from_file(self, path: str|Path) -> Self:
        access = ClusterAccess.mock(path)
        return self.fill_from_store(access)

    def fill_from_env(self) -> Self:
        return self._fill(lambda val: val.fill_from_env())

    def fill_from_dict(self, paths: dict[str,Any]) -> Self:
        return self._fill(lambda val: val.fill_from_dict(paths))

    def fill_from_args(self) -> Self:
        paths = {}
        for arg in args:
            if "=" not in arg:
                continue
            key, val = arg.split("=")
            paths[key] = val

        return self.fill_from_dict(paths)

    def override_from_args(self, args: list[str]) -> Self:
        for arg in args:
            if "=" not in arg:
                continue
            key, val = arg.split("=")
            keys = key.split("/")
            try:
                self.set_nested(keys, val)
            except Exception as e:
                self._logger.warning(f"Could not set the value of key {key}:\n{e}")

        return self


default_kafka_consumer_config = Config.from_dict({
    "bootstrap.servers": Wants.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
    "group.id": "eo4eu",
    'enable.auto.commit': False,
    "auto.offset.reset": "latest",
})

default_kafka_producer_config = Config.from_dict({
    "bootstrap.servers": Wants.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
})

default_boto_config = Config.from_dict({
    "region_name":           Wants.cfgmap("s3-access", "region_name"),
    "endpoint_url":          Wants.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Wants.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Wants.secret("s3-access-scr", "aws_secret_access_key"),
})

default_cloud_config = Config.from_dict({
    "endpoint_url":          Wants.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Wants.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Wants.secret("s3-access-scr", "aws_secret_access_key"),
})

default_eo4eu_config = Config.from_dict({
    "namespace":      Wants.cfgmap("eo4eu", "namespace"),
    "s3_bucket_name": Wants.cfgmap("eo4eu", "s3-bucket-name"),
})
