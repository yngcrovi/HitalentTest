from sqlalchemy import select, text, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db.model import DepartmentModel
from db.config.engine import EngineDB
from pathlib import Path
from typing import Literal

class DepartmentService:
    
    def __init__(self):
        self.session = EngineDB().get_engine()
        self.table = DepartmentModel
        self.SQL_DIR = Path(__file__).parent.parent / "sql"

    def load_sql_query(self, filename: str) -> str:
        file_path = self.SQL_DIR / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    async def check_exist_department(self, id: int = None, name: str = None, parent_id: int = None) -> bool:
        async with self.session as s:
            query = select(self.table)
            if id:
                query = select(self.table).where(self.table.id==id)
            elif name:
                query = select(self.table).where(self.table.name==name)
            elif parent_id:
                query = select(self.table).where(self.table.parent_id==parent_id)
            result = await s.execute(query)
            return result.scalar_one_or_none()

    async def create_department(self, name: str, parent_id: int = None) -> dict:
        try:
            async with self.session as s:
                if await self.check_exist_department(name=name, parent_id=parent_id):
                    raise HTTPException(status_code=409, detail="Такое подразделение уже существует")
                obj = self.table(name=name, parent_id=parent_id)
                s.add(obj)
                await s.flush()
                if parent_id == obj.id:
                    raise HTTPException(status_code=409, detail="Подразделение не может быть родителем самого себя")
                await s.commit()
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "parent_id": obj.parent_id,
                    "created_at": obj.created_at
                }
        except IntegrityError as e:
            original_error = e.orig
            if "ForeignKeyViolationError" in str(original_error) and "parent_id" in str(original_error):
                raise HTTPException(
                    status_code=400,
                    detail=f"Родительский отдел с id={parent_id} не существует"
                )
            else: 
                raise HTTPException(
                        status_code=400,
                        detail=f"{str(e)}"
                    )
            
    async def get_department_tree(self, id: int, depth: int) -> dict:
        async with self.session as s:
            if not await self.check_exist_department(id=id):
                raise HTTPException(status_code=404, detail="Такого подразделеня не существует")
            engine = s.get_bind()
            if "sqlite" in str(engine.url):
                sql_file = "department_tree.sqlite.sql"
            else:
                sql_file = "department_tree.postgresql.sql"
            query = text(self.load_sql_query(sql_file))
            
            result = await s.execute(query, {
                "dept_id": id, 
                "depth": depth
            })
            
            rows = result.fetchall()
            data = {
                "departments_id": []
            }
            for row in rows:
                dep = {
                    "id": row.id,
                    "name": row.name,
                    "parent_id": row.parent_id,
                    "created_at": row.created_at,
                }
                if row.level == 0:
                    data["main"] = dep
                else:
                    if data.get(row.level):
                        data[row.level].append(dep)
                    else:
                        data[row.level] = [dep]
                data["departments_id"].append(row.id)

            return data
        
    async def move_department(self, id: int, name: str | None, parent_id: int | None):
        if not await self.check_exist_department(id=id):
            raise HTTPException(status_code=404, detail="Такого подразделеня не существует")
        if not await self.check_exist_department(id=parent_id):
            raise HTTPException(status_code=404, detail="Такого родительского подразделеня не существует")
        if id == parent_id:
            raise HTTPException(status_code=409, detail="Подразделение не может быть родителем самого себя")
        async with self.session as s:
            result = await s.execute(select(self.table).where(self.table.id==id))
            obj = result.scalar_one_or_none()
            obj.parent_id = parent_id
            if name:
                obj.name = name
            await s.execute(update(self.table).where(self.table.id==parent_id).values(parent_id=None))
            await s.commit()
            await s.refresh(obj)
            return {
                "id": obj.id,
                "name": obj.name,
                "parent_id": obj.parent_id,
                "created_at": obj.created_at
            }
        
    async def delete_department(self, id: int):
        async with self.session as s:
            await s.execute(delete(self.table).where(self.table.id==id))
            await s.commit()
        