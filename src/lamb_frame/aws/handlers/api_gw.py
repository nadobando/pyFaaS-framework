import abc

from pydantic import BaseModel, ValidationError

from ...handlers import BaseFunctionHandler
from ...exceptions import BaseLambdaError
from ...middlewares import HttpCorrelationIdMiddleware
from ...requests import AwsApiGatewayHttpRequest
from ...responses import HttpResponse, Errors, Error, ValidateError
from ...typing import Union


class LambdaProxyHandler(BaseFunctionHandler, abc.ABC):
    request_class = AwsApiGatewayHttpRequest
    response_class = HttpResponse
    middlewares = (HttpCorrelationIdMiddleware(),)
    body_class: BaseModel = None
    path_params_class: BaseModel = None
    query_string_class: BaseModel = None
    body = None
    __params_list__ = []

    def __serialize_request__(self, request, context):
        if not issubclass(self.request_class, AwsApiGatewayHttpRequest):
            raise Exception(f"request must be subclass of {AwsApiGatewayHttpRequest.__name__}")
        self.__params_list__ = []
        self.request = self.request_class.parse_request(request)

        if self.body_class is not None:
            try:
                self.request.body = self.body_class.parse_obj(self.request.body)
                self.__params_list__.append(self.request.body)
            except ValidationError as e:
                self.logger.error("error in body")
                raise e

        if self.path_params_class is not None:
            self.request.params = self.path_params_class.parse_obj(self.request.params)
            self.__params_list__.append(self.request.params)

        if self.query_string_class is not None:
            try:
                self.request.query_str = self.query_string_class.parse_obj(self.request.query_str)
                self.__params_list__.append(self.request.query_str)
            except ValidationError as e:
                self.logger.error("error in qs")
                raise e

    def __process_handle__(self):
        try:
            return self.handle(*self.__params_list__)
        except TypeError as e:
            import re
            match = re.match("handle\(\) takes \d+ positional arguments but \d+ were given", str(e))
            if match:
                raise Exception(
                    "Your handler must include positional arguments as set on (body_class, path_params_class, query_string_class)")
            else:
                raise e

    def handle_error(self, error: Union[Exception, BaseLambdaError, ValidationError]) -> HttpResponse:
        response = HttpResponse.construct()
        response.set_header("x-amzn-ErrorType", type(error).__name__)
        response.set_header("x-amzn-RequestId", self.context.aws_request_id)
        try:
            raise error
        except BaseLambdaError:
            response.body = Errors(errors=[Error(type=type(error).__name__, message=str(error))])
            response.status_code = error.status_code
            return response()
        except ValidationError as e:
            response.body = Errors(
                errors=[ValidateError(loc=i['loc'], type=i['type'], message=i['msg']) for i in e.errors()])
            response.status_code = 400
            Error(type=type(e).__name__, message=e.errors())
        except Exception as e:
            response.body = Errors(errors=[Error(type=type(e).__name__, message="Internal Server Error")])
            response.status_code = 500

        return response
