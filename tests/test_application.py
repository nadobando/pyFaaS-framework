import importlib
import os

import pytest

from faas_framework.handlers import BaseFunctionHandler


class MyTestHandler(BaseFunctionHandler):
    def __serialize_request__(self, request, context):
        pass

    def __process_handle__(self):
        pass

    def __process_response__(self, response):
        pass

    def handle(self, *args, **kwargs):
        pass

    def handle_error(self, error: Exception):
        pass


class NotBaseFunctionHandler:
    pass


def test_no_class_handler_raises_exception():
    with pytest.raises(Exception):
        importlib.import_module("faas_framework.app")


def test_class_handler_not_BaseFunctionHandler():
    os.environ["CLASS_HANDLER"] = "test_application.NotBaseFunctionHandler"
    with pytest.raises(Exception) as e:
        importlib.import_module("faas_framework.app")

    assert str(e.value) == f"handle must be subclass of {BaseFunctionHandler.__name__}"


def test_app():
    os.environ["CLASS_HANDLER"] = "test_application.MyTestHandler"
    importlib.import_module("faas_framework.app")
