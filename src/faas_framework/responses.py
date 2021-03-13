import abc
from collections import deque
from datetime import datetime

from pydantic import BaseModel

from . import typing
from .models import CamelCasedModel, Field
from .typing import DataT
from .utils.collections import CaseInsensitiveDict


class Error(BaseModel):
    type: str
    message: typing.Union[str, typing.List[str]]


class ValidateError(Error):
    loc: typing.List[typing.Union[str, int]]


class Errors(BaseModel):
    timestamp: datetime = datetime.utcnow()
    errors: typing.List[typing.Union[Error, ValidateError]]

    class Config:
        json_encoders = {datetime: lambda x: f"{str(x)[:10]}T{str(x)[11:23]}+0000"}


class Response(BaseModel):
    status_code: int = Field(200, ge=200, le=505)
    body: typing.Optional[DataT] = None

    def __call__(self, *args, **kwargs):
        return self.dict(exclude_none=True)


class HttpResponse(Response, CamelCasedModel, abc.ABC):
    headers: typing.MutableMapping[str, typing.Set[str]] = None

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def set_header(
        self, key: str, value: typing.Union[str, int, float, bool, typing.List]
    ):
        if self.headers is None:
            self.headers = CaseInsensitiveDict()
        if key not in self.headers:
            self.headers[key] = set()

        if type(value) is not list:
            self.headers[key].add(value)
        else:
            deque(map(self.headers[key].add, value))

    def set_cookie(
        self,
        key,
        value,
        *,
        expires: datetime = None,
        max_age: int = None,
        domain: str = None,
        path: str = None,
        secure: bool = False,
        http_only: bool = False,
        same_site: typing.Literal["Strict", "Lax", "None"] = None,
    ):
        cookie = [f"{key}={value}"]
        cookie.append(f"Expires={str(expires)}") if expires else None
        cookie.append(f"Max-Age={str(max_age)}") if max_age else None
        cookie.append(f"Domain={domain}") if domain else None
        cookie.append(f"Path={path}") if path else None
        cookie.append("Secure") if secure else None
        cookie.append("HttpOnly") if http_only else None
        cookie.append(f"SameSite={same_site}") if same_site else None

        self.set_header("Set-Cookie", ";".join(cookie))

        # if "set-cookie" not in self.headers:
        #     self.headers['Set-Cookie'] = set()
        # self.headers['Set-Cookie'].add(f"{key}={value}")
