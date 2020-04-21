import abc
from collections import deque

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, BaseSettings

from .middlewares import BaseMiddleware
from .responses import Response
from .typing import Tuple, Dict, Any

logger: Logger = Logger()


class BaseFunctionHandler(abc.ABC):
    request_class: BaseModel = None
    response_class: BaseModel = Response
    settings_class: BaseSettings = None
    default_middlewares: Tuple[BaseMiddleware] = ()
    middlewares: Tuple[BaseMiddleware] = ()
    logger = logger

    # sts_sessions: typing.Tuple[AssumableSession] = tuple()

    def __init__(self):
        self.raw_request = None
        self.request = None
        self.context = None
        if callable(self.settings_class):
            self.settings = self.settings_class()

    def __call__(self, request: Dict[str, Any], context: LambdaContext):
        self.raw_request = request
        self.context = context
        return self.__handle()

    @abc.abstractmethod
    def __serialize_request__(self, request, context):
        """
        template method pattern for the framework
        """
        pass

    @abc.abstractmethod
    def __process_handle__(self):
        return self.handle(self.request)

    def __handle(self):
        self.logger.info(self.raw_request)

        # try:
        deque(map(lambda x: x.on_request(self), self.middlewares))
        # self.request = self.__serialize_request__(self.raw_request, self.context)
        self.__serialize_request__(self.raw_request, self.context)
        _response = self.__process_handle__()

        if _response is None:
            _response = self.response_class()
        if not issubclass(_response.__class__, Response):
            _response = self.response_class(body=_response)

        deque(map(lambda x: x.on_response(_response), self.middlewares))
        # except Exception as e:
        #     self.logger.exception("Exception thrown")
        #     _response = self.handle_error(e)

        return _response()

    @abc.abstractmethod
    def handle(self, *args, **kwargs):
        """
        here goes the lambda implementation
        """
        pass

    @abc.abstractmethod
    def handle_error(self, error: Exception):
        """
        general error handling
        TODO: how to make it general for all lambda not only api-gw
        """
        # return Response(status_code=500, error=Error(type=type(error).__name__, message="Internal Server Error"))()
