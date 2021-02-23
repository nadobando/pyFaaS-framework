import abc
import base64
import json
import uuid
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError

from ...exceptions import BaseFunctionError, SerializationError
from ...handlers import BaseFunctionHandler
from ...middlewares import BaseMiddleware
from ...models import CamelCasedModel
from ...requests import HttpRequest
from ...responses import Errors, Error, ValidateError, HttpResponse
from ...typing import Union, Tuple, Any
from ...utils.collections import CaseInsensitiveDict


@dataclass
class AwsApiGatewayHttpRequest(HttpRequest):

    @classmethod
    def __handle_body__(cls, body, is_base_64, headers: CaseInsensitiveDict):
        _body = body if not is_base_64 else base64.b64decode(body)
        content_type = headers.get('content-type')
        if content_type and content_type[0]:
            func = cls.__mapping__.get(content_type[0])
            if func:
                _body = func(_body)

        return _body

    @classmethod
    def parse_request(cls, request):
        headers = request['multiValueHeaders']
        qs_params = request['multiValueQueryStringParameters'] if request['multiValueQueryStringParameters'] else {}
        query_str = {
            x: y[0] for x, y in qs_params.items() if len(y) == 1
        }
        qs_params.update(query_str)
        path_params = request['pathParameters']
        headers = CaseInsensitiveDict(**headers) if headers else {}
        body = cls.__handle_body__(request['body'], request['isBase64Encoded'], headers)
        _request = dict(
            path=request['path'],
            headers=headers,
            query_str=qs_params,
            params=path_params if path_params else {},
            body=body,
            method=request['httpMethod']

        )
        return cls(**_request)


class AwsApiGwHttpResponse(HttpResponse, CamelCasedModel):
    is_base64_encoded: bool = False

    def __call__(self, *args, **kwargs):
        _dict = self.dict(exclude_none=True)
        try:
            if hasattr(self.body, 'json'):
                _dict['body'] = self.body.json(exclude_none=True)
            elif type(self.body) is str:
                _dict['body'] = self.body
            else:
                _dict['body'] = json.dumps(self.body)
        except TypeError as e:
            raise SerializationError(type(self.body).__name__)

        if self.headers is not None:
            _dict['multiValueHeaders'] = {k: list(v) for k, v in _dict.pop('headers').items()}
        return _dict


class HttpCorrelationIdMiddleware(BaseMiddleware):
    # correlation_id: str
    header = "X-Correlation-Id"

    def on_request(self):
        self.handler.correlation_id = self.handler.raw_request['multiValueHeaders'].get(self.header, None)
        if self.handler.correlation_id is None:
            self.handler.correlation_id = str(uuid.uuid4())

    def on_response(self, response: AwsApiGwHttpResponse):
        response.set_header(self.header, self.handler.correlation_id)


class LambdaApiGwProxyHandler(BaseFunctionHandler, abc.ABC):
    middlewares = (HttpCorrelationIdMiddleware(),)
    request_class = AwsApiGatewayHttpRequest
    response_class = AwsApiGwHttpResponse
    body_class: BaseModel = None
    path_params_class: BaseModel = None
    query_string_class: BaseModel = None
    # headers_class: BaseModel = None
    body: Union[BaseModel, str] = None

    __params_list__ = []
    __params_str_list = []

    def __serialize_request__(self, request, context):
        if not issubclass(self.request_class, AwsApiGatewayHttpRequest):
            raise Exception(f"request must be subclass of {AwsApiGatewayHttpRequest.__name__}")
        self.__params_list__ = []
        self.request = self.request_class.parse_request(request)
        if self.body_class is not None:
            try:
                self.request.body = self.body_class.parse_obj(self.request.body)
                self.__params_list__.append(self.request.body)
                self.__params_str_list.append('body')
            except ValidationError as e:
                self.logger.exception("error in body")
                raise e
        else:
            self.__params_list__.append(self.request.body)

        # if self.headers_class is not None:
        #     self.request.headers = self.headers_class.parse_obj(self.request.headers)

        if self.path_params_class is not None:
            try:
                self.request.params = self.path_params_class.parse_obj(self.request.params)
                self.__params_list__.append(self.request.params)
                self.__params_str_list.append('path_params')
            except ValidationError as e:
                self.logger.error("error in path params")
                raise e

        if self.query_string_class is not None:
            try:
                self.request.query_str = self.query_string_class.parse_obj(self.request.query_str)
                self.__params_list__.append(self.request.query_str)
                self.__params_str_list.append('query_string')
            except ValidationError as e:
                self.logger.error("error in qs")
                raise e

    def __process_handle__(self):
        try:
            return self.handle(*self.__params_list__)
        except TypeError as e:
            import re
            match = re.match(r'handle\(\) takes \d+ positional arguments? but \d+ were given', str(e))
            if match:
                raise Exception(
                    f"Your handler must include positional arguments as set on ({','.join(self.__params_str_list)})")
            else:
                raise e

    @abc.abstractmethod
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        pass

    def handle_error(self, error: Union[Exception, BaseFunctionError, ValidationError]) -> AwsApiGwHttpResponse:
        response = AwsApiGwHttpResponse.construct()
        response.set_header("x-amzn-ErrorType", type(error).__name__)
        response.set_header("x-amzn-RequestId", self.context.aws_request_id)
        try:
            raise error
        except BaseFunctionError:
            response.body = Errors(errors=[Error(type=type(error).__name__, message=str(error))])
            response.status_code = error.status_code
            return response
        except ValidationError as e:
            response.body = Errors(
                errors=[ValidateError(loc=i['loc'], type=i['type'], message=i['msg']) for i in e.errors()])
            response.status_code = 400
        except Exception as e:
            response.body = Errors(errors=[Error(type=type(e).__name__, message="Internal Server Error")])
            response.status_code = 500

        return response

    def __process_response__(self, response: Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]) -> AwsApiGwHttpResponse:
        if isinstance(response, AwsApiGwHttpResponse):
            return response
        if isinstance(response, tuple):
            length = len(response)
            if length == 2:
                return AwsApiGwHttpResponse(status_code=response[0], body=response[1])

        # default
        return AwsApiGwHttpResponse(status_code=200, body=response)
