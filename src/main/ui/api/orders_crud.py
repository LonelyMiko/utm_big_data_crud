import os

import fastapi.routing
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from src.main.ui.models import OrderModel, UpdateOrderModel
from src.main.db.connector import DBConnector


async def get_orders(db_conn):
    orders = await db_conn.retrieve_orders()
    return orders


db = DBConnector(conn_id=os.getenv("DB_CONN"))
router = fastapi.routing.APIRouter(prefix="/api/v1", tags=["orders"])


@router.post("/orders", response_description="Add new order")
async def create_order(order: OrderModel = Body(...)):
    order = jsonable_encoder(order)
    new_order = await db.add_order(order)
    return new_order


@router.get("/orders", response_description="List orders with pagination")
async def get_orders(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    orders = await db.retrieve_orders(skip=skip, limit=limit)
    return orders


@router.get("/orders/{id}", response_description="Read a single order")
async def get_order(id: str):
    order = await db.retrieve_order(id)
    if order:
        return order
    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@router.put("/orders", response_description="Update an order")
async def update_order(id: str = Query(), order: UpdateOrderModel = Body(...)):
    order_data = {k: v for k, v in order.dict().items() if v is not None}
    if len(order_data) >= 1:
        updated = await db.update_order(id, order_data)
        if updated:
            updated_order = await db.retrieve_order(id)
            return updated_order
    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@router.delete("/orders", response_description="Delete an order")
async def delete_order(id: str = Query()):
    deleted = await db.delete_order(id)
    if deleted:
        return {"message": f"Order {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Order {id} not found")
