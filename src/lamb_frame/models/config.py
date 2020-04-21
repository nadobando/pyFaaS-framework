import pydantic
from pydantic.generics import GenericModel

from .. import typing
from ..utils.functions import camelcase, titlecase

__PYDANTIC_BASE_MODEL__ = pydantic.BaseModel


class CamelCaseConfig(pydantic.BaseConfig):
    alias_generator = camelcase
    allow_population_by_field_name = True


class TitleCaseConfig(pydantic.BaseConfig):
    alias_generator = titlecase
    allow_population_by_field_name = True


class BaseModel(pydantic.BaseModel):
    def dict(self, *, include: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
             exclude: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
             by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False,
             exclude_defaults: bool = False, exclude_none: bool = False, ) -> 'DictStrAny':
        return super().dict(
            include=include,
            exclude=exclude,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            by_alias=True
        )


class CamelCasedModel(BaseModel):
    Config = CamelCaseConfig


class TitleCaseModel(BaseModel):
    Config = TitleCaseConfig


class CamelCaseGenericModel(GenericModel):
    Config = CamelCaseConfig

    def dict(self, *, include: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
             exclude: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
             by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False,
             exclude_defaults: bool = False, exclude_none: bool = False, ) -> 'DictStrAny':
        return super().dict(
            include=include,
            exclude=exclude,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            by_alias=True
        )

