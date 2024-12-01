import os

import fastapi.routing
from fastapi import HTTPException, Query
from src.main.db.connector import DBConnector
from src.main.ui.models import DepartmentModel, UpdateDepartmentModel

db = DBConnector(conn_id=os.getenv("DB_CONN"))
departments_router = fastapi.routing.APIRouter(prefix="/api/v1", tags=["departments"])


@departments_router.post("/departments", response_description="Add new department")
async def create_department(department: DepartmentModel):
    new_department = await db.add_department(department.dict())
    return new_department


@departments_router.get("/departments", response_description="List departments with pagination")
async def get_departments(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    result = await db.retrieve_departments(skip=skip, limit=limit)
    return result


@departments_router.get("/departments/{id}", response_description="Get a single department")
async def get_department(id: str):
    department = await db.retrieve_department(id)
    if department:
        return department
    raise HTTPException(status_code=404, detail=f"Department {id} not found")


@departments_router.put("/departments", response_description="Update a department")
async def update_department(department: UpdateDepartmentModel, id: str = Query()):
    department_data = {k: v for k, v in department.model_dump().items() if v is not None}
    if len(department_data) >= 1:
        updated = await db.update_department(id, department_data)
        if updated:
            updated_department = await db.retrieve_department(id)
            return updated_department
    raise HTTPException(status_code=404, detail=f"Department {id} not found")


@departments_router.delete("/departments", response_description="Delete a department")
async def delete_department(id: str = Query()):
    deleted = await db.delete_department(id)
    if deleted:
        return {"message": f"Department {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Department {id} not found")
