import abc


class BaseMiddleware(abc.ABC):
    handler: 'BaseFunctionHandler'

    @abc.abstractmethod
    def on_request(self):
        pass

    @abc.abstractmethod
    def on_response(self, response):
        pass
