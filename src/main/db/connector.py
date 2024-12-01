from typing import Any, Mapping, List, Dict

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
import logging

import math


def order_helper(order) -> dict:
    days_since_prior_order = order.get("days_since_prior_order")
    if isinstance(days_since_prior_order, float) and math.isnan(days_since_prior_order):
        days_since_prior_order = None
    return {
        "id": str(order["_id"]),
        "order_id": order["order_id"],
        "user_id": order["user_id"],
        "eval_set": order["eval_set"],
        "order_number": order["order_number"],
        "order_dow": order["order_dow"],
        "order_hour_of_day": order["order_hour_of_day"],
        "days_since_prior_order": days_since_prior_order,
    }


def aisle_helper(aisle) -> dict:
    return {
        "id": str(aisle["_id"]),
        "aisle_id": aisle["aisle_id"],
        "aisle": aisle["aisle"]
    }


def department_helper(department) -> dict:
    return {
        "id": str(department["_id"]),
        "department_id": department["department_id"],
        "department": department["department"]
    }


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "aisle_id": product["aisle_id"],
        "department_id": product["department_id"]
    }


def order_helper(order) -> dict:
    days_since_prior_order = order.get("days_since_prior_order")
    if isinstance(days_since_prior_order, float) and math.isnan(days_since_prior_order):
        days_since_prior_order = None
    return {
        "id": str(order["_id"]),
        "order_id": order["order_id"],
        "user_id": order["user_id"],
        "eval_set": order["eval_set"],
        "order_number": order["order_number"],
        "order_dow": order["order_dow"],
        "order_hour_of_day": order["order_hour_of_day"],
        "days_since_prior_order": days_since_prior_order,
    }


class DBConnector:
    def __init__(self, conn_id: str, db_name: str = "instacart_db"):
        if conn_id and conn_id.startswith("mongodb"):
            try:
                self.conn_id = conn_id
                self.client = AsyncIOMotorClient(conn_id)
                self.database = self.client[db_name]
                self.orders_collection = self.database.get_collection('orders')
                self.orders_train_collection = self.database.get_collection("orders_train")
                self.aisles_collection = self.database.get_collection('aisles')
                self.departments_collection = self.database.get_collection('departments')
                self.products_collection = self.database.get_collection('products')
            except Exception as e:
                logging.error(f"Error on creating connector: {str(e)}")
                raise
        else:
            raise ValueError("conn_id is not valid")

    async def retrieve_orders(self, skip: int = 0, limit: int = 10) -> dict:
        orders = []
        cursor = self.orders_collection.find().skip(skip).limit(limit)
        async for order in cursor:
            orders.append(order_helper(order))
        total_orders = await self.orders_collection.count_documents({})
        return {
            "total": total_orders,
            "skip": skip,
            "limit": limit,
            "orders": orders
        }

    async def retrieve_order(self, id: str) -> Mapping[str, Any] | None:
        order = await self.orders_collection.find_one({"_id": ObjectId(id)})
        if order:
            return order_helper(order)
        return None

    async def add_order(self, order_data: dict) -> dict:
        order = await self.orders_collection.insert_one(order_data)
        new_order = await self.orders_collection.find_one({"_id": order.inserted_id})
        return order_helper(new_order)

    async def update_order(self, id: str, data: dict) -> bool:
        if len(data) < 1:
            return False
        result = await self.orders_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete_order(self, id: str) -> bool:
        result = await self.orders_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def retrieve_aisles(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        aisles = []
        cursor = self.aisles_collection.find().skip(skip).limit(limit)
        async for aisle in cursor:
            aisles.append(aisle_helper(aisle))
        total_aisles = await self.aisles_collection.count_documents({})
        return {
            "total": total_aisles,
            "skip": skip,
            "limit": limit,
            "aisles": aisles
        }

    async def retrieve_aisle(self, id: str) -> Mapping[str, Any]:
        aisle = await self.aisles_collection.find_one({"_id": ObjectId(id)})
        if aisle:
            return aisle_helper(aisle)
        return None

    async def add_aisle(self, aisle_data: dict) -> dict:
        aisle = await self.aisles_collection.insert_one(aisle_data)
        new_aisle = await self.aisles_collection.find_one({"_id": aisle.inserted_id})
        return aisle_helper(new_aisle)

    async def update_aisle(self, id: str, data: dict) -> bool:
        if len(data) < 1:
            return False
        result = await self.aisles_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete_aisle(self, id: str) -> bool:
        result = await self.aisles_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    # Departments CRUD methods
    async def retrieve_departments(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        departments = []
        cursor = self.departments_collection.find().skip(skip).limit(limit)
        async for department in cursor:
            departments.append(department_helper(department))
        total_departments = await self.departments_collection.count_documents({})
        return {
            "total": total_departments,
            "skip": skip,
            "limit": limit,
            "departments": departments
        }

    async def retrieve_department(self, id: str) -> Mapping[str, Any]:
        department = await self.departments_collection.find_one({"_id": ObjectId(id)})
        if department:
            return department_helper(department)
        return None

    async def add_department(self, department_data: dict) -> dict:
        department = await self.departments_collection.insert_one(department_data)
        new_department = await self.departments_collection.find_one({"_id": department.inserted_id})
        return department_helper(new_department)

    async def update_department(self, id: str, data: dict) -> bool:
        if len(data) < 1:
            return False
        result = await self.departments_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete_department(self, id: str) -> bool:
        result = await self.departments_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    # Products CRUD methods
    async def retrieve_products(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        products = []
        cursor = self.products_collection.find().skip(skip).limit(limit)
        async for product in cursor:
            products.append(product_helper(product))
        total_products = await self.products_collection.count_documents({})
        return {
            "total": total_products,
            "skip": skip,
            "limit": limit,
            "products": products
        }

    async def retrieve_product(self, id: str) -> Mapping[str, Any]:
        product = await self.products_collection.find_one({"_id": ObjectId(id)})
        if product:
            return product_helper(product)
        return None

    async def add_product(self, product_data: dict) -> dict:
        product = await self.products_collection.insert_one(product_data)
        new_product = await self.products_collection.find_one({"_id": product.inserted_id})
        return product_helper(new_product)

    async def update_product(self, id: str, data: dict) -> bool:
        if len(data) < 1:
            return False
        result = await self.products_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete_product(self, id: str) -> bool:
        result = await self.products_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def get_orders_dataframe(self) -> List[Dict[str, Any]]:
        cursor = self.orders_collection.find({}, {
            "_id": 0,
            "order_id": 1,
            "user_id": 1,
            "eval_set": 1,
            "order_number": 1,
            "order_dow": 1,
            "order_hour_of_day": 1,
            "days_since_prior_order": 1
        })
        orders = await cursor.to_list(length=10000)
        return orders

    async def get_order_products_dataframe(self) -> List[Dict[str, Any]]:
        cursor = self.orders_train_collection.find({}, {
            "_id": 0,
            "order_id": 1,
            "product_id": 1,
            "add_to_cart_order": 1,
            "reordered": 1
        })
        order_products = await cursor.to_list(length=10000)
        return order_products

    async def get_products_dataframe(self) -> List[Dict[str, Any]]:
        cursor = self.products_collection.find({}, {
            "_id": 0,
            "product_id": 1,
            "product_name": 1,
            "aisle_id": 1,
            "department_id": 1
        })
        products = await cursor.to_list(length=10000)
        return products

    async def get_aisles_dataframe(self) -> List[Dict[str, Any]]:
        cursor = self.aisles_collection.find({}, {
            "_id": 0,
            "aisle_id": 1,
            "aisle": 1
        })
        aisles = await cursor.to_list(length=1000)
        return aisles

    async def get_departments_dataframe(self) -> List[Dict[str, Any]]:
        cursor = self.departments_collection.find({}, {
            "_id": 0,
            "department_id": 1,
            "department": 1
        })
        departments = await cursor.to_list(length=10000)
        return departments
