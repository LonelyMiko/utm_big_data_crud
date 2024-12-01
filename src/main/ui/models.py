from pydantic import BaseModel
from typing import Optional


class OrderModel(BaseModel):
    order_id: int
    user_id: int
    eval_set: str
    order_number: int
    order_dow: int
    order_hour_of_day: int
    days_since_prior_order: Optional[float]


class UpdateOrderModel(BaseModel):
    eval_set: Optional[str]
    order_number: Optional[int]
    order_dow: Optional[int]
    order_hour_of_day: Optional[int]
    days_since_prior_order: Optional[float]


class AisleModel(BaseModel):
    aisle_id: int
    aisle: str


class UpdateAisleModel(BaseModel):
    aisle: Optional[str]


class DepartmentModel(BaseModel):
    department_id: int
    department: str


class UpdateDepartmentModel(BaseModel):
    department: Optional[str]


class ProductModel(BaseModel):
    product_id: int
    product_name: str
    aisle_id: int
    department_id: int


class UpdateProductModel(BaseModel):
    product_name: Optional[str]
    aisle_id: Optional[int]
    department_id: Optional[int]
