from typing import get_origin
from fastapi import Request
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo
from pydantic.alias_generators import to_camel


class QueryParameterModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @classmethod
    def parser(cls, request: Request):
        obj: dict = {}
        for field in cls.model_fields:
            fieldInfo: FieldInfo = cls.model_fields[field]
            if get_origin(fieldInfo.annotation) is list:
                alias = f"{fieldInfo.alias}[]"
                obj[field] = cls._get_values_by_alias(alias, request)
                continue

            if fieldInfo.alias is not None and fieldInfo.alias in request.query_params:
                obj[field] = cls._get_value_by_alias(
                    fieldInfo=fieldInfo, request=request
                )

        return cls(**dict(obj))

    @classmethod
    def _get_value_by_alias(cls, fieldInfo: FieldInfo, request: Request):
        return request.query_params[fieldInfo.alias]

    @classmethod
    def _get_values_by_alias(cls, alias: str, request: Request):
        return [
            value
            for pair in request.url.query.split("&")
            if pair.startswith(f"{alias}=")
            for value in pair.split("=")[1:]
        ]

    def __init__(self, **pydict):
        super().__init__(**pydict)
