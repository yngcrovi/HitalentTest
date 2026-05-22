from fastapi import APIRouter, Query, Depends, HTTPException, Response
from .model import NewDepartmentModel, DepartmentResponseModel, EmployeesModel, EmployeesResponseModel, GetDepartmentsTreeResponseModel, MoveDepartmentModel, DeleteDepartmentModel
from db.service import DepartmentService, EmployeeService

route = APIRouter(
    prefix="/departments",
    tags=['Department']
)

@route.post("/", response_model=DepartmentResponseModel)
async def create_department(data: NewDepartmentModel, department_service: DepartmentService = Depends(DepartmentService)): 
    return await department_service.create_department(data.name, data.parent_id)

@route.post("/{id}/employees/", response_model=EmployeesResponseModel)
async def create_employees(
    data: EmployeesModel, id: int, department_service: DepartmentService = Depends(DepartmentService), employee_service: EmployeeService = Depends(EmployeeService)
): 
    if not await department_service.check_exist_department(id=id):
        raise HTTPException(status_code=404, detail="Такого подразделения нет")
    return await employee_service.create_employee(data.model_dump(), id)

@route.get("/{id}", response_model=GetDepartmentsTreeResponseModel, response_model_exclude_none=True)
async def get_department(
    id: int, depth: int = Query(default=1, le=5),  include_employees: bool = True, department_service: DepartmentService = Depends(DepartmentService), 
    employee_service: EmployeeService = Depends(EmployeeService)
): 
    data = {}
    departments = await department_service.get_department_tree(id, depth)
    data["department"] = departments["main"]
    data["children"] = {i+1: departments[i+1] for i in range(depth) if departments.get(i+1)}
    if include_employees:
        data["employees"] = await employee_service.get_employees_department(departments["departments_id"])
    return data

@route.patch("/{id}", response_model=DepartmentResponseModel)
async def move_department(id: int, data: MoveDepartmentModel, department_service: DepartmentService = Depends(DepartmentService)):
    return await department_service.move_department(id, data.name, data.parent_id)

@route.delete("/{id}", response_model=DepartmentResponseModel)
async def delete_department(
    id: int, data: DeleteDepartmentModel, department_service: DepartmentService = Depends(DepartmentService), employee_service: EmployeeService = Depends(EmployeeService)                        
):
    if data.reassign_to_department_id and data.mode != "cascade":
        if not await department_service.check_exist_department(id=data.reassign_to_department_id):
            raise HTTPException(status_code=404, detail="Подразделения, в которое вы хотите перевести, не существует")
        await employee_service.reassign_employees(id, data.reassign_to_department_id)
    await department_service.delete_department(id)
    return Response(status_code=204)