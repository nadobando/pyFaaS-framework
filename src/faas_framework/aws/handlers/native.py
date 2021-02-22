import abc
from typing import Tuple

from ...handlers import BaseFunctionHandler


class NativeHandler(BaseFunctionHandler, abc.ABC):
    middlewares: Tuple = None

    def __process_handle__(self):
        return super().__process_handle__()

    def __serialize_request__(self, request, context):
        if self.request_class is not None:
            self.request = self.request_class.parse_obj(request)
        else:
            self.request = request

    def __process_response__(self, response):
        return super(NativeHandler, self).__process_response__(response)

    def handle_error(self, error: Exception) -> str:
        return str(error)
