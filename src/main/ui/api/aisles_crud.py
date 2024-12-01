import os

import fastapi.routing
from fastapi import HTTPException, Query
from src.main.db.connector import DBConnector
from src.main.ui.models import AisleModel, UpdateAisleModel


db = DBConnector(conn_id=os.getenv("DB_CONN"))
aisle_router = fastapi.routing.APIRouter(prefix="/api/v1", tags=["aisles"])


@aisle_router.post("/aisles", response_description="Add new aisle")
async def create_aisle(aisle: AisleModel):
    new_aisle = await db.add_aisle(aisle.dict())
    return new_aisle


@aisle_router.get("/aisles", response_description="List aisles with pagination")
async def get_aisles(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    result = await db.retrieve_aisles(skip=skip, limit=limit)
    return result


@aisle_router.get("/aisles/{id}", response_description="Read a single aisle")
async def get_aisle(id:str):
    aisle = await db.retrieve_aisle(id)
    if aisle:
        return aisle
    raise HTTPException(status_code=404, detail=f"Aisle {id} not found")


@aisle_router.put("/aisles", response_description="Update an aisle")
async def update_aisle(aisle: UpdateAisleModel, id: str = Query()):
    aisle_data = {k: v for k, v in aisle.dict().items() if v is not None}
    if len(aisle_data) >= 1:
        updated = await db.update_aisle(id, aisle_data)
        if updated:
            updated_aisle = await db.retrieve_aisle(id)
            return updated_aisle
    raise HTTPException(status_code=404, detail=f"Aisle {id} not found")


@aisle_router.delete("/aisles", response_description="Delete an aisle")
async def delete_aisle(id: str = Query()):
    deleted = await db.delete_aisle(id)
    if deleted:
        return {"message": f"Aisle {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Aisle {id} not found")
