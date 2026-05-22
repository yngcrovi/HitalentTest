from . import AsyncClient

class TestDepartmentAPI:

    async def test_create_department_success(self, client: AsyncClient):
        response = await client.post("/api/departments/", json={"name": "IT отдел"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IT отдел"
        assert data["parent_id"] is None
        assert "id" in data

    async def test_create_employee_success(self, client: AsyncClient):
        dept_resp = await client.post("/api/departments/", json={"name": "IT"})
        dept_id = dept_resp.json()["id"]
        response = await client.post(
            f"/api/departments/{dept_id}/employees/",
            json={"full_name": "Иван Иванов", "position": "Разработчик"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Иван Иванов"
        assert data["department_id"] == dept_id

    async def test_get_department_success(self, client: AsyncClient):
        dept_resp = await client.post("/api/departments/", json={"name": "HR"})
        dept_id = dept_resp.json()["id"]

        await client.post(
            f"/api/departments/{dept_id}/employees/",
            json={"full_name": "Анна Смирнова", "position": "HR-менеджер"}
        )

        response = await client.get(f"/api/departments/{dept_id}?depth=1&include_employees=true")
        assert response.status_code == 200
        data = response.json()
        assert data["department"]["name"] == "HR"
        assert len(data["employees"]) == 1

    async def test_move_department_success(self, client: AsyncClient):
        parent_resp = await client.post("/api/departments/", json={"name": "Главный"})
        parent_id = parent_resp.json()["id"]

        child_resp = await client.post("/api/departments/", json={"name": "Дочерний"})
        child_id = child_resp.json()["id"]

        response = await client.patch(
            f"/api/departments/{child_id}",
            json={"parent_id": parent_id}
        )
        assert response.status_code == 200
        assert response.json()["parent_id"] == parent_id

    async def test_delete_department_cascade_success(self, client: AsyncClient):
        dept_resp = await client.post("/api/departments/", json={"name": "Удаляемый отдел"})
        dept_id = dept_resp.json()["id"]

        response = await client.request(
            method="DELETE",
            url=f"/api/departments/{dept_id}",
            json={"mode": "cascade"}
        )
        assert response.status_code == 204

        get_response = await client.get(f"/api/departments/{dept_id}")
        assert get_response.status_code == 404