import pytest

from faas_framework.exceptions import BaseFunctionError


class MyTestFunctionError(BaseFunctionError):
    message = "hello {name}"
    status_code = 400


class MyTestFunctionErrorIgnoreParams(BaseFunctionError):
    message = "hello"
    status_code = 400


class MyTestFunctionErrorWithoutParams(BaseFunctionError):
    message = "hello {name}"
    status_code = 400


@pytest.mark.parametrize(
    "exc,params,expected_msg",
    [
        (MyTestFunctionError, {"name": "world"}, "hello world"),
        (MyTestFunctionErrorIgnoreParams, {"name": "world"}, "hello"),
    ],
)
def test_base_function_error(exc, params, expected_msg):
    with pytest.raises(BaseFunctionError) as e:
        raise exc(**params)

    assert str(e.value) == expected_msg


def test_base_all_params_set():
    with pytest.raises(Exception) as x:
        raise MyTestFunctionErrorWithoutParams()

    with pytest.raises(TypeError) as y:
        str(x.value)

    assert (
        str(y.value)
        == "MyTestFunctionErrorWithoutParams missing 1 required keyword-only argument: {'name'}"
    )


@pytest.mark.parametrize(
    "exc,args,params,expected_msg",
    [
        (
            MyTestFunctionError,
            ("changed exception message",),
            {"name": "world"},
            "changed exception message",
        ),
        (
            MyTestFunctionError,
            ("changed exception message with {param}",),
            {"param": "value"},
            "changed exception message with value",
        ),
    ],
)
def test_changed_msg(exc, args, params, expected_msg):
    with pytest.raises(BaseFunctionError) as e:
        raise exc(*args, **params)

    assert str(e.value) == expected_msg
