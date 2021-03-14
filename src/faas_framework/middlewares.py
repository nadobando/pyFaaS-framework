import abc

# from .handlers import BaseFunctionHandler


class BaseMiddleware(abc.ABC):
    handler: "BaseFunctionHandler"  # noqa: F821

    @abc.abstractmethod
    def on_request(self):
        pass

    @abc.abstractmethod
    def on_response(self, response):
        pass
