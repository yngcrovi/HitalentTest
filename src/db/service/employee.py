from sqlalchemy import select, insert, and_, func, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db.model import EmployeeModel
from db.config.engine import EngineDB
from uuid import UUID

class EmployeeService:
    
    def __init__(self):
        self.session = EngineDB().get_engine()
        self.table = EmployeeModel

    async def check_exist_employee(self, full_name: str) -> EmployeeModel | None:
        async with self.session as s:
            query = select(self.table).where(self.table.full_name==full_name)
            result = await s.execute(query)
            return result.one_or_none()

    async def create_employee(self, data: dict, department_id: int) -> dict:
        async with self.session as s:
            if await self.check_exist_employee(data["full_name"]):
                result = await s.execute(
                    select(self.table).where(
                        self.table.full_name == data["full_name"]
                    )
                )
                obj = result.scalar_one_or_none()
                obj.department_id = department_id
                obj.position = data["position"]
                obj.hired_at = data["hired_at"]
                await s.commit()
                await s.refresh(obj)
            else:
                obj = self.table(**data, department_id=department_id)
                s.add(obj)
                await s.flush()
                await s.commit()
            return {
                "id": obj.id,
                "department_id": obj.department_id,
                "full_name": obj.full_name,
                "position": obj.position,
                "hired_at": obj.hired_at,
                "created_at": obj.created_at
            }
        
    async def get_employees_department(self, departments_id: list[int]):
        async with self.session as s:
            engine = s.get_bind()
            if "sqlite" in str(engine.url):
                hired_at_formatted = func.strftime('%d.%m.%Y', self.table.hired_at).label('hired_at')
                created_at_formatted = func.strftime('%d.%m.%Y %H:%M:%S', self.table.created_at).label('created_at')
            else:
                hired_at_formatted = func.to_char(self.table.hired_at, 'DD.MM.YYYY').label('hired_at')
                created_at_formatted = func.to_char(self.table.created_at, 'DD.MM.YYYY HH24:MI:SS').label('created_at')
            query = select(
                    self.table.id, 
                    self.table.full_name,
                    self.table.position,
                    self.table.department_id,
                    hired_at_formatted,
                    created_at_formatted
                ).where(self.table.department_id.in_(departments_id))
            result = await s.execute(query)
            return result.mappings().all()
        
    async def reassign_employees(self, old_department_id: int, new_department_id: int):
        async with self.session as s:
            await s.execute(update(self.table).where(self.table.department_id==old_department_id).values(department_id=new_department_id))
            await s.commit()