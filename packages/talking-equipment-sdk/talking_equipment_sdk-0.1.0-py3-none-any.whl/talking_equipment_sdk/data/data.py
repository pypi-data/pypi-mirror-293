import json
from abc import ABC
from typing import Union, Any

from pydantic import BaseModel, field_validator, ValidationError

from talking_equipment_sdk.data.enums import DataValueType


class BaseDataModel(BaseModel, ABC):
    @staticmethod
    def _convert_value(value: Any, data_model_class) -> Any:
        if value is None:
            return None
        else:
            return value if isinstance(value, data_model_class) else data_model_class(value)


class DataModel(BaseDataModel, ABC):
    value: Union[int, float, str, bool]
    value_type: DataValueType = None
    unit_name: str = ''
    unit_abbreviation: str = ''

    def __init__(self, value: Union[int, float, str], **kwargs):
        super().__init__(value=value, **kwargs)

    def __str__(self):
        return self.value_verbose

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        value_type = cls.model_fields['value_type'].default

        if value_type is None:
            raise ValidationError(f'Value type is required for {cls.__name__}')

        if value_type == DataValueType.BOOL:
            return bool(v)

        if value_type == DataValueType.INT:
            return int(v)

        if value_type == DataValueType.FLOAT:
            return float(v)

        if value_type == DataValueType.STR:
            return str(v)

        return v

    @classmethod
    @property
    def value_type_str(cls) -> str:
        return cls.value_type.__name__

    @property
    def value_verbose(self) -> str:
        return f'{self.value}{self.unit_abbreviation}'

    @property
    def value_verbose_full(self) -> str:
        return f'{self.value} {self.unit_name}'

    @property
    def is_bool(self) -> bool:
        return isinstance(self.value, bool)

    @property
    def is_float(self) -> bool:
        return isinstance(self.value, float)

    @property
    def is_int(self) -> bool:
        return isinstance(self.value, int)

    @property
    def is_json(self) -> bool:
        try:
            json.loads(self.value)
            return True
        except ValueError:
            return False

    @property
    def is_str(self) -> bool:
        return isinstance(self.value, str)


class DataModelContainer(BaseDataModel, ABC):
    value_type: DataValueType = DataValueType.JSON

    @property
    def value(self):
        return self.model_dump_json()