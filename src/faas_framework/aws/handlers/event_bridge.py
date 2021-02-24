import abc

from faas_framework.aws.handlers.native import NativeHandler
from faas_framework.aws.models.event_bridge import EventBridgeModel


# from faas_framework.handlers import BaseFunctionHandler


class EventBridgeHandler(NativeHandler, abc.ABC):
    request_class = EventBridgeModel

