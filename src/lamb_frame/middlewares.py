import abc
import uuid

from .responses import HttpResponse


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    def on_request(self, handler):
        pass

    @abc.abstractmethod
    def on_response(self, response):
        pass


class HttpCorrelationIdMiddleware(BaseMiddleware):
    correlation_id: str
    header = "X-Correlation-Id"

    def on_request(self, handler):
        self.correlation_id = handler.raw_request['multiValueHeaders'].get(self.header, None)
        if self.correlation_id is None:
            self.correlation_id = str(uuid.uuid4())
        handler.correlation_id = self.correlation_id

    def on_response(self, response: HttpResponse):
        response.set_header(self.header, self.correlation_id)


class ClientContextCorrelationIdMiddleware(BaseMiddleware):
    correlation_id: str = None
    field = 'correlationId'

    def on_request(self, handler):
        if hasattr(handler.context, "client_context"):
            if hasattr(handler.context.client_context, "custom"):
                self.correlation_id = handler.context.client_context.custom.get(self.field, None)

        if self.correlation_id is None:
            self.correlation_id = str(uuid.uuid4())

        handler.correlation_id = self.correlation_id

    def on_response(self, response):
        response.add_metadata(self.field, self.correlation_id)
