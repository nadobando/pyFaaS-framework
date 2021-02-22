import pytest

from faas_framework.utils.functions import camelcase, title_case


@pytest.mark.parametrize("str_in,str_out", [
    ("hello", "hello"),
    ("hello_world", "helloWorld"),
    ("Lorem_ipsum_dolor_sit_amet", "loremIpsumDolorSitAmet"),
    (None, "none"),


])
def test_camelcase(str_in, str_out):
    assert camelcase(str_in) == str_out


@pytest.mark.parametrize("str_in,str_out", [
    ("hello", "Hello"),
    ("hello_world", "HelloWorld"),
    ("Lorem_ipsum_dolor_sit_amet", "LoremIpsumDolorSitAmet")
])
def test_title_case(str_in, str_out):
    assert title_case(str_in) == str_out
