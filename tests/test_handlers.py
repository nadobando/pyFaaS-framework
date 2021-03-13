import os
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, BaseSettings
from pytest_mock import MockerFixture

from faas_framework.aws.handlers.native import NativeHandler
from faas_framework.middlewares import BaseMiddleware


class MySettings(BaseSettings):
    some_setting: str


class MyModel(BaseModel):
    name: str


class BasicImplementationFunctionHandler(NativeHandler):
    settings_class = MySettings

    def handle(self, *args, **kwargs):
        return {"hello": "world"}


class RequestClassFunctionHandler(BasicImplementationFunctionHandler):
    request_class = MyModel


class ErrorInFunctionHandler(BasicImplementationFunctionHandler):
    def handle(self, *args, **kwargs):
        raise Exception("this exception should trigger handler_error function")


class MyMiddleware(BaseMiddleware):
    def on_request(self):
        self.handler.moto = "Go Serverless"

    def on_response(self, response):
        response["moto"] = self.handler.moto


class MiddlewaredHandler(BasicImplementationFunctionHandler):
    middlewares = (MyMiddleware(),)


os.environ["some_setting"] = "some value"
basic_implementation_function_handler = BasicImplementationFunctionHandler()
request_class_function_handler = RequestClassFunctionHandler()
error_in_function_handler = ErrorInFunctionHandler()
middlewared_handler = MiddlewaredHandler()


class TestBaseFunctionHandler:
    @pytest.mark.parametrize(
        "handler,req,expected",
        [
            (basic_implementation_function_handler, {1, 2, 3}, {1, 2, 3}),
            (
                request_class_function_handler,
                {"name": "lamb-frame"},
                MyModel(name="lamb-frame"),
            ),
        ],
    )
    def test_request_serialization(
        self, handler: BasicImplementationFunctionHandler, req, expected
    ):
        handler.__serialize_request__(req, {})
        assert handler.request == expected, "unequal value"
        assert type(handler.request) == type(expected), "unequal type"

    def test_handle_error(self, lambda_context, mocker: MockerFixture):
        mocker.patch.object(error_in_function_handler, "handle_error")

        error_in_function_handler({}, lambda_context)
        # noinspection PyTypeHints
        error_in_function_handler.handle_error: MagicMock
        error_in_function_handler.handle_error.assert_called_once()

    def test_middlewares(self, lambda_context):
        response = middlewared_handler({}, lambda_context)
        assert "moto" in response
        assert response["moto"] == "Go Serverless"

    def test_handler_settings(self):
        assert basic_implementation_function_handler.settings
        assert (
            basic_implementation_function_handler.settings.some_setting == "some value"
        )
