import abc
import json
from dataclasses import dataclass

from . import typing


@dataclass
class HttpRequest(abc.ABC):
    path: str
    method: typing.Literal["HEAD", "GET", "POST", "PUT", "PATCH", "OPTIONS", "CONNECT", "TRACE", "DELETE"]
    headers: typing.Mapping[str, typing.List[str]] = None
    query_str: typing.Optional[typing.Mapping[str, typing.List[str]]] = None
    params: typing.Optional[typing.Mapping[str, str]] = None
    body: typing.Any = None
    __mapping__ = {
        "application/json": json.loads,
    }

    @classmethod
    def parse_request(cls, request):
        ...
