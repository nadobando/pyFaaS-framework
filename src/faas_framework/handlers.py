import abc
from collections import deque

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, BaseSettings

from .middlewares import BaseMiddleware
from .typing import Any, Dict, Tuple

logger: Logger = Logger()


class BaseFunctionHandler(abc.ABC):
    request_class: BaseModel = None
    settings_class: BaseSettings = None
    middlewares: Tuple[BaseMiddleware] = ()
    logger = logger

    def __init__(self):
        self.raw_request = None
        self.request = None
        self.context = None
        if callable(self.settings_class):
            self.settings = self.settings_class()

    def __post_init__(self):
        pass

    def __call__(self, request: Dict[str, Any], context: LambdaContext):
        self.raw_request = request
        self.context = context
        self.__post_init__()
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
            self.logger.exception("Exception thrown")
            response = self.handle_error(e)
            # raise e
        finally:
            if self.middlewares:
                deque(map(lambda x: x.on_response(response), self.middlewares))

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
        """
        pass
