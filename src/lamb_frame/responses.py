import json
from collections import deque
from datetime import datetime

from pydantic import BaseModel

from . import typing
from .exceptions import SerializationError
from .models import Field, validator, CamelCasedModel
from .utils.collections import CaseInsensitiveDict

DataT = typing.TypeVar('DataT')


class Error(BaseModel):
    type: str
    message: typing.Union[str, typing.List[str]]


class ValidateError(Error):
    loc: typing.List[typing.Union[str, int]]


class Errors(BaseModel):
    timestamp: datetime = datetime.utcnow()
    errors: typing.List[typing.Union[Error, ValidateError]]

    class Config:
        json_encoders = {
            datetime: lambda x: f'{str(x)[:10]}T{str(x)[11:23]}+0000'
        }


class Response(BaseModel):
    status_code: int = Field(200, ge=200, le=505)
    body: typing.Optional[DataT] = None

    def __call__(self, *args, **kwargs):
        return self.dict(exclude_none=True)


class IntegrationResponse(Response, typing.Generic[DataT]):
    metadata = dict()
    errors: typing.List[Error] = None

    @classmethod
    @validator('error', always=True)
    def check_consistency(cls, v, values):
        if v is not None and values['data'] is not None:
            raise ValueError('must not provide both data and error')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def __call__(self, *args, **kwargs):
        if len(self.metadata) == 0:
            self.metadata = None
        return self.dict(exclude_none=True)


class HttpResponse(Response, CamelCasedModel):
    headers: typing.MutableMapping[str, typing.Set[str]] = None
    is_base64_encoded: bool = False

    # body: typing.Optional[DataT]
    # status_code: int = Field(200, ge=200, le=505)

    def __call__(self, *args, **kwargs):
        _dict = self.dict(exclude_none=True)
        try:
            if hasattr(self.body, 'json'):
                _dict['body'] = self.body.json(exclude_none=True)
            else:
                _dict['body'] = json.dumps(self.body)
        except TypeError as e:
            raise SerializationError(type(self.body).__name__)

        if self.headers is not None:
            _dict['multiValueHeaders'] = {k: list(v) for k, v in _dict.pop('headers').items()}
        return _dict

    def set_header(self, key: str, value: typing.Union[str, int, float, bool, typing.List]):
        if self.headers is None:
            self.headers = CaseInsensitiveDict()
        if key not in self.headers:
            self.headers[key] = set()

        if type(value) is not list:
            self.headers[key].add(value)
        else:
            deque(map(self.headers[key].add, value))

    def set_cookie(self, key, value, *, expires: datetime = None, max_age: int = None, domain: str = None,
                   path: str = None, secure: bool = False, http_only: bool = False,
                   same_site: typing.Literal["Strict", "Lax", "None"] = None, ):
        cookie = [f"{key}={value}"]
        cookie.append(f"Expires={str(expires)}") if expires else None
        cookie.append(f"Max-Age={str(max_age)}") if max_age else None
        cookie.append(f"Domain={domain}") if domain else None
        cookie.append(f"Path={path}") if path else None
        cookie.append(f"Secure") if secure else None
        cookie.append(f"HttpOnly") if http_only else None
        cookie.append(f"SameSite={same_site}") if same_site else None

        self.set_header("Set-Cookie", ";".join(cookie))

        # if "set-cookie" not in self.headers:
        #     self.headers['Set-Cookie'] = set()
        # self.headers['Set-Cookie'].add(f"{key}={value}")
