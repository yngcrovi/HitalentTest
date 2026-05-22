from pydantic import BaseModel, Field, field_validator, field_serializer, model_validator
from datetime import datetime
from typing import Literal

class NewDepartmentModel(BaseModel):
    name: str = Field(
        min_length=1, 
        max_length=200
    )
    parent_id: int | None  = None

    @field_validator('name')
    @classmethod
    def trim_name(cls, v: str) -> str:
        """Убирает лишние пробелы: удаляет пробелы в начале и конце"""
        return v.strip()
    
class MoveDepartmentModel(NewDepartmentModel):
    name: str = Field(
        min_length=1, 
        max_length=200,
        default=None
    )

class DepartmentResponseModel(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    created_at: datetime

    @field_serializer('created_at')
    def serialize_created_at(self, dt: datetime) -> str:
        return dt.strftime('%d.%m.%Y %H:%M:%S')

class GetDepartmentsTreeResponseModel(BaseModel):
    department: dict
    employees: list[dict] | None = None
    children: dict[int, list]

class DeleteDepartmentModel(BaseModel):
    mode: Literal['cascade', 'reassign']
    reassign_to_department_id: int = Field(
        ge=1,
        default=None
    )

    @model_validator(mode='after')
    def validate_reassign(self):
        if self.mode == 'reassign' and self.reassign_to_department_id is None:
            raise ValueError('При mode="reassign" необходимо указать reassign_to_department_id')
        return self
