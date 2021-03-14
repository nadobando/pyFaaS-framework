from typing import Any, Callable, Optional, Union

import pydantic

from .. import typing
from ..utils.functions import camelcase, title_case

__PYDANTIC_BASE_MODEL__ = pydantic.BaseModel


class CamelCaseConfig(pydantic.BaseConfig):
    alias_generator = camelcase
    allow_population_by_field_name = True


class TitleCaseConfig(pydantic.BaseConfig):
    alias_generator = title_case
    allow_population_by_field_name = True


class AliasedBaseModel(pydantic.BaseModel):
    def dict(  # noqa: A003
        self,
        *,
        include: typing.Union[
            "AbstractSetIntStr", "DictIntStrAny"  # noqa: F821
        ] = None,
        exclude: typing.Union[
            "AbstractSetIntStr", "DictIntStrAny"  # noqa: F821
        ] = None,
        by_alias: bool = True,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":  # noqa: F821
        return super().dict(
            include=include,
            exclude=exclude,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            by_alias=True,
        )

    def json(
        self,
        *,
        include: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,  # noqa: F821
        exclude: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,  # noqa: F821
        by_alias: bool = True,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        **dumps_kwargs: Any,
    ) -> str:
        return super().json(
            include=include,
            exclude=exclude,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            by_alias=by_alias,
        )


class CamelCasedModel(AliasedBaseModel):
    Config = CamelCaseConfig


class TitleCaseModel(AliasedBaseModel):
    Config = TitleCaseConfig


# class CamelCaseGenericModel(GenericModel):
#     Config = CamelCaseConfig
#
#     def dict(self, *, include: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
#              exclude: typing.Union['AbstractSetIntStr', 'DictIntStrAny'] = None,
#              by_alias: bool = True, skip_defaults: bool = None, exclude_unset: bool = False,
#              exclude_defaults: bool = False, exclude_none: bool = False, ) -> 'DictStrAny':
#         return super().dict(
#             include=include,
#             exclude=exclude,
#             skip_defaults=skip_defaults,
#             exclude_unset=exclude_unset,
#             exclude_defaults=exclude_defaults,
#             exclude_none=exclude_none,
#             by_alias=True
#         )
