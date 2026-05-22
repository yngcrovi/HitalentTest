from pydantic import BaseModel, Field
from datetime import date, datetime

class EmployeesModel(BaseModel):
    full_name: str = Field(
        min_length=1, 
        max_length=200,
    )
    position: str = Field(
        min_length=1, 
        max_length=200,
    )
    hired_at: date | None = None

class EmployeesResponseModel(EmployeesModel):
    id: int
    department_id: int
    created_at: datetime