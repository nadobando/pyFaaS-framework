import importlib
import os

from .handlers import BaseFunctionHandler

__class_handler_field__ = "CLASS_HANDLER"


def __import_handler__(class_handler: str):
    module, split, cls_str = class_handler.rpartition(".")
    imported_module = importlib.import_module(module)
    cls = imported_module.__getattribute__(cls_str)
    if not issubclass(cls, BaseFunctionHandler):
        raise Exception(f"handle must be subclass of {BaseFunctionHandler.__name__}")
    return cls()


__class_handler_str__ = os.environ.get(__class_handler_field__, None)
if __class_handler_str__ is None:
    raise Exception(f"You must provide {__class_handler_field__} environment variable")
handler = __import_handler__(__class_handler_str__)
