import abc

from pydantic import ValidationError

from ...handlers import BaseFunctionHandler
from ...exceptions import BaseLambdaError
from ...middlewares import ClientContextCorrelationIdMiddleware
from ...responses import IntegrationResponse, Response, Error, ValidateError


class NativeHandler(BaseFunctionHandler, abc.ABC):
    middlewares = (ClientContextCorrelationIdMiddleware(),)
    response_class = IntegrationResponse

    def __process_handle__(self):
        return super().__process_handle__()

    def __serialize_request__(self, request, context):
        if self.request_class is not None:
            self.request = self.request_class.parse_obj(request)
        else:
            self.request = request

    def handle_error(self, error: BaseLambdaError) -> Response:
        response = self.response_class()
        try:
            raise error
        except BaseLambdaError:
            response.errors = [Error(type=type(error).__name__, message=str(error))]
            response.status_code = error.status_code
            return response()
        except ValidationError as e:
            response.errors = [ValidateError(loc=i['loc'], type=i['type'], message=i['msg']) for i in e.errors()]
            response.status_code = 400
            Error(type=type(e).__name__, message=e.errors())
        except Exception as e:
            response.errors = [Error(type=type(e).__name__, message="Internal Server Error")]
            response.status_code = 500

        return response
