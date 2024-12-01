import os

import fastapi.routing
from fastapi import HTTPException, Query
from src.main.db.connector import DBConnector
from src.main.ui.models import ProductModel, UpdateProductModel

db = DBConnector(conn_id=os.getenv("DB_CONN"))
products_router = fastapi.routing.APIRouter(prefix="/api/v1", tags=["products"])


@products_router.post("/products", response_description="Add new product")
async def create_product(product: ProductModel):
    new_product = await db.add_product(product.dict())
    return new_product


@products_router.get("/products", response_description="List products with pagination")
async def get_products(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    result = await db.retrieve_products(skip=skip, limit=limit)
    return result


@products_router.get("/products/{id}", response_description="Get a single product")
async def get_product(id: str):
    product = await db.retrieve_product(id)
    if product:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@products_router.put("/products", response_description="Update a product")
async def update_product(product: UpdateProductModel, id: str = Query()):
    product_data = {k: v for k, v in product.dict().items() if v is not None}
    if len(product_data) >= 1:
        updated = await db.update_product(id, product_data)
        if updated:
            updated_product = await db.retrieve_product(id)
            return updated_product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@products_router.delete("/products", response_description="Delete a product")
async def delete_product(id: str = Query()):
    deleted = await db.delete_product(id)
    if deleted:
        return {"message": f"Product {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
