import pytest
from pydantic import ValidationError

from faas_framework.models import CamelCasedModel, TitleCaseModel


class MyCamelCasedModel(CamelCasedModel):
    very_long_field_name: str


class MyTitleCasedModel(TitleCaseModel):
    very_long_field_name: str


@pytest.mark.parametrize("cls,obj", [
    (MyCamelCasedModel, {"veryLongFieldName": "should pass"}),
    (MyTitleCasedModel, {"VeryLongFieldName": "should pass"})

])
def test_model_alias_works(cls, obj):
    cls.parse_obj(obj)
    assert True


@pytest.mark.parametrize("cls,obj", [
    (MyCamelCasedModel, {"VeryLongFieldName": "should pass"}),
    (MyTitleCasedModel, {"veryLongFieldName": "should pass"})

])
def test_model_alias_fails(cls, obj):
    with pytest.raises(ValidationError):
        test_model_alias_works(cls, obj)
