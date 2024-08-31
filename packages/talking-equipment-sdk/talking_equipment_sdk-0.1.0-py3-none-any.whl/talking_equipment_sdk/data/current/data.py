from dataclasses import dataclass
from typing import Union

from pydantic import field_validator

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer


class CurrentData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit: str = 'Amps'
    unit_abbreviation: str = 'A'

    def __post_init__(self):
        self.value = float(self.value)


class ThreePhaseCurrentData(ThreePhaseDataContainer):
    a: Union[CurrentData, float, int]
    b: Union[CurrentData, float, int]
    c: Union[CurrentData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, CurrentData)