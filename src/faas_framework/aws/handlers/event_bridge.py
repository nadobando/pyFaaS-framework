import abc

from faas_framework.aws.handlers.native import NativeHandler
from faas_framework.aws.models.event_bridge import EventBridgeModel
# from faas_framework.handlers import BaseFunctionHandler
from faas_framework.handlers import BaseFunctionHandler
from faas_framework.models.config import BaseModel


class EventBridgeHandler(NativeHandler, abc.ABC):
    request_class = EventBridgeModel
    detail_class: BaseModel

    def __serialize_request__(self, request, context):
        if not issubclass(self.request_class, EventBridgeModel):
            raise Exception(f"request must be subclass of {EventBridgeModel.__name__}")
        self.request: EventBridgeModel = self.request_class.parse_obj(request)
        if self.detail_class:
            self.request.detail = self.detail_class.parse_obj(self.request.detail)
        else:
            self.detail = self.request.detail
