import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


class MockLambdaContext(LambdaContext):
    def __init__(
        self, function_name, invoked_function_arn, aws_request_id, memory_limit=128
    ):
        self._function_name = function_name
        self._memory_limit_in_mb = memory_limit
        self._invoked_function_arn = invoked_function_arn
        self._aws_request_id = aws_request_id


@pytest.fixture
def lambda_context() -> LambdaContext:
    fn_arn = "arn:aws:lambda:us-east-1:12345678:function:test-fn"
    aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"
    return MockLambdaContext("test-fn", fn_arn, aws_request_id)
