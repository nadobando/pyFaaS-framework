import re
from typing import Union, Tuple, Any, List
from uuid import UUID

import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, create_model, ValidationError

from faas_framework.aws.handlers.api_gw import AwsApiGwHttpResponse, LambdaApiGwProxyHandler
from faas_framework.exceptions import BaseLambdaError
from faas_framework.models.config import CamelCasedModel

timestamp_pattern = re.compile(r".*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{4}).*")


class MyTestModel(CamelCasedModel):
    customer_id: UUID


class PathParamsModel(BaseModel):
    param: str


class QueryStringParams(BaseModel):
    parameter1: List[str]
    parameter2: str


class MyLambdaProxyHandler(LambdaApiGwProxyHandler):
    def handle(self, body, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return body


class ProxyHandler(LambdaApiGwProxyHandler):
    body_class = MyTestModel
    path_params_class = PathParamsModel
    query_string_class = QueryStringParams

    def handle(self, body, path_params, query_string, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return 200, body


class BadHandlerSignatureHandler(LambdaApiGwProxyHandler):

    def handle(self, body, path_params, query_string, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        pass


class BadOverriddenRequestClass(MyLambdaProxyHandler):
    response_class = object


class BadQueryStringRequestHandler(MyLambdaProxyHandler):
    query_string_class = create_model("BadParamModel", not_exists=(str, ...))


class BadBodyRequestHandler(MyLambdaProxyHandler):
    body_class = create_model("BadParamModel", not_exists=(str, ...))


class BadPathParamRequestHandler(MyLambdaProxyHandler):
    path_params_class = create_model("BadParamModel", not_exists=(str, ...))


class NoHttpResponseHandler(LambdaApiGwProxyHandler):
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return {"some_key": "some_value"}


class TupleResponse(LambdaApiGwProxyHandler):
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return 300, {"some_key": "some_value"}


class HttpResponseHandler(LambdaApiGwProxyHandler):
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return AwsApiGwHttpResponse(body={"some_key": "some_value"}, status_code=202)


class HttpDefaultResponseHandler(LambdaApiGwProxyHandler):
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        return AwsApiGwHttpResponse(body={"some_key": "some_value"})


class ErrorResponse(LambdaApiGwProxyHandler):
    def handle(self, *args, **kwargs) -> Union[AwsApiGwHttpResponse, Tuple[int, Any], Any]:
        raise BaseLambdaError("this is the error message", status_code=409)
        # return Error(type="SomeErrorType", message="this is a the error type")


def is_str(obj):
    return type(obj) is str


body_payload = '{"customerId": "6e83612e-4b68-4a0a-aadb-53a5bbce7c7f"}'


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize("event,expected_output,handler", [
    (pytest.lazy_fixture("api_gw_event_dict_str_body"), "Hello from Lambda!", MyLambdaProxyHandler()),
    (pytest.lazy_fixture("api_gw_event_dict_json_body"), body_payload, ProxyHandler()),
    (pytest.lazy_fixture("api_gw_event_dict_json_base64_body"), body_payload, ProxyHandler()),
])
def test_handler(event, expected_output, handler, ):
    # noinspection PyTypeChecker
    response = handler(event, LambdaContext())
    assert response['body']
    assert is_str(response['body'])
    assert response['body'] == expected_output


exception_calls = [
    (Exception, BadOverriddenRequestClass),
    (ValidationError, BadQueryStringRequestHandler),
    (ValidationError, BadBodyRequestHandler),
    (ValidationError, BadPathParamRequestHandler),
    (Exception, BadHandlerSignatureHandler)
]


@pytest.mark.parametrize('exc,handler', exception_calls)
def test_exceptions(exc, handler, api_gw_event_dict_json_body, lambda_context):
    try:
        handler()(api_gw_event_dict_json_body, lambda_context)
    except Exception as e:
        assert type(e) is exc, f"exception not as expected: {str(e)}"


@pytest.mark.parametrize("handler_class,expected_response", [
    (NoHttpResponseHandler, AwsApiGwHttpResponse(body={"some_key": "some_value"})),
    (TupleResponse, AwsApiGwHttpResponse(body={"some_key": "some_value"}, status_code=300)),
    (HttpResponseHandler, AwsApiGwHttpResponse(body={"some_key": "some_value"}, status_code=202)),
    (HttpDefaultResponseHandler, AwsApiGwHttpResponse(body={"some_key": "some_value"}, status_code=200)),

])
def test_responses(handler_class, expected_response, api_gw_event_dict_json_body, lambda_context):
    response = handler_class()(api_gw_event_dict_json_body, lambda_context)
    headers = "multiValueHeaders"

    if response[headers]:
        for header, value in response[headers].items():
            expected_response.set_header(header, value)
    assert response == expected_response()


@pytest.mark.parametrize("handler_class,expected_response", [
    (ErrorResponse, AwsApiGwHttpResponse(body={"timestamp": "2021-02-21T11:40:38.568+0000",
                                               "errors": [{"type": "BaseLambdaError",
                                                           "message": "this is the error message"}]},
                                         status_code=409))
])
def test_error_response(handler_class, expected_response, api_gw_event_dict_json_body, lambda_context):
    response = handler_class()(api_gw_event_dict_json_body, lambda_context)
    headers = "multiValueHeaders"
    if response[headers]:
        for header, value in response[headers].items():
            expected_response.set_header(header, value)

    ts = timestamp_pattern.match(response['body'])
    expected_response.body['timestamp'] = ts.groups()[0]
    assert response == expected_response()
