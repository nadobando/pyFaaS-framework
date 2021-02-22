import abc
from collections import deque

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, BaseSettings

from .middlewares import BaseMiddleware
from .typing import Tuple, Dict, Any

logger: Logger = Logger()


class BaseFunctionHandler(abc.ABC):
    request_class: BaseModel = None
    # response_class: Union[BaseModel, Any] = None
    settings_class: BaseSettings = None
    # default_middlewares: Tuple[BaseMiddleware] = ()
    middlewares: Tuple[BaseMiddleware] = ()
    logger = logger

    def __init__(self):
        self.raw_request = None
        self.request = None
        self.context = None
        if callable(self.settings_class):
            self.settings = self.settings_class()

    def __call__(self, request: Dict[str, Any], context: LambdaContext):
        self.raw_request = request
        self.context = context
        response = self.__handle()
        return response

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

        try:
            if self.middlewares:
                for i in self.middlewares:
                    i.handler = self
                    i.on_request()

            self.__serialize_request__(self.raw_request, self.context)
            response = self.__process_handle__()
            response = self.__process_response__(response)

        except Exception as e:
            self.logger.exception("Exception thrown in handle")
            response = self.handle_error(e)
            # raise e
        try:
            deque(map(lambda x: x.on_response(response), self.middlewares))
        except Exception as e:
            self.logger.exception("Exception thrown in response middleware")

        return response() if callable(response) else response

    @abc.abstractmethod
    def __process_response__(self, response):
        return response

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
