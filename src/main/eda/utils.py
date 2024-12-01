from typing import Dict, Any
import pandas as pd
from src.main.db.connector import DBConnector
import asyncio

class DataAnalysis:
    def __init__(self, conn_id: str):
        self.db_connector = DBConnector(conn_id)
        # DataFrames will be initialized as None
        self.orders_df = None
        self.order_products_df = None
        self.products_df = None
        self.aisles_df = None
        self.departments_df = None

    async def load_dataframes(self):
        if self.orders_df is None:
            orders = await self.db_connector.get_orders_dataframe()
            self.orders_df = pd.DataFrame(orders)
        if self.order_products_df is None:
            order_products = await self.db_connector.get_order_products_dataframe()
            self.order_products_df = pd.DataFrame(order_products)
        if self.products_df is None:
            products = await self.db_connector.get_products_dataframe()
            self.products_df = pd.DataFrame(products)
        if self.aisles_df is None:
            aisles = await self.db_connector.get_aisles_dataframe()
            self.aisles_df = pd.DataFrame(aisles)
        if self.departments_df is None:
            departments = await self.db_connector.get_departments_dataframe()
            self.departments_df = pd.DataFrame(departments)

    async def analyze_hypothesis1(self) -> Dict[str, Any]:
        await self.load_dataframes()

        merged_df = self.order_products_df.merge(self.products_df, on="product_id")
        merged_df = merged_df.merge(self.aisles_df, on="aisle_id")
        merged_df = merged_df.merge(self.departments_df, on="department_id")

        order_aisles = merged_df.groupby('order_id')['aisle'].apply(set).reset_index()

        # Calculate the frequency of orders where products from the same aisle appear together
        total_orders = order_aisles.shape[0]
        same_aisle_orders = order_aisles[order_aisles['aisle'].apply(lambda x: len(x) == 1)].shape[0]

        percentage_same_aisle = (same_aisle_orders / total_orders) * 100

        return {
            "total_orders": total_orders,
            "same_aisle_orders": same_aisle_orders,
            "percentage_same_aisle": percentage_same_aisle,
        }

    async def analyze_hypothesis2(self) -> Dict[str, Any]:
        await self.load_dataframes()

        total_products = self.order_products_df.shape[0]
        reordered_products = self.order_products_df[self.order_products_df['reordered'] == 1].shape[0]

        percentage_reordered = (reordered_products / total_products) * 100

        return {
            "total_products": total_products,
            "reordered_products": reordered_products,
            "percentage_reordered": percentage_reordered,
        }

    async def analyze_hypothesis3(self) -> Dict[str, Any]:
        await self.load_dataframes()

        # aisles_id IDs for fruits, eggs, bread
        aisles_id = [24, 36, 94]

        # Get product IDs for basic products
        basic_products = self.products_df[self.products_df['aisle_id'].isin(aisles_id)]['aisle_id'].tolist()

        # Merge dataframes
        merged_df = self.order_products_df.merge(self.orders_df, on="order_id")
        basic_orders = merged_df[merged_df['product_id'].isin(basic_products)]

        # Categorize orders by time of day
        basic_orders['time_of_day'] = basic_orders['order_hour_of_day'].apply(
            lambda x: 'Morning' if 5 <= x < 12 else 'Evening' if 17 <= x <= 23 else 'Other'
        )

        morning_count = basic_orders[basic_orders['time_of_day'] == 'Morning'].shape[0]
        evening_count = basic_orders[basic_orders['time_of_day'] == 'Evening'].shape[0]

        return {
            "morning_count": morning_count,
            "evening_count": evening_count,
        }

    async def analyze_hypothesis4(self) -> Dict[str, Any]:
        await self.load_dataframes()

        # Merge dataframes
        merged_df = self.order_products_df.merge(self.products_df, on="product_id")
        merged_df = merged_df.merge(self.departments_df, on="department_id")

        order_stats = merged_df.groupby('order_id').agg(
            total_products=('product_id', 'count'),
            unique_departments=('department_id', 'nunique')
        ).reset_index()

        correlation = order_stats['total_products'].corr(order_stats['unique_departments'])

        return {
            "average_departments": order_stats['unique_departments'].mean(),
            "correlation": correlation,
        }

    async def analyze_hypothesis5(self) -> Dict[str, Any]:
        await self.load_dataframes()

        merged_df = self.order_products_df.merge(self.orders_df, on="order_id")

        merged_df['is_weekend'] = merged_df['order_dow'].apply(lambda x: x in [0, 1])

        order_counts = merged_df.groupby(['order_id', 'is_weekend']).size().reset_index(name='product_count')

        avg_weekend = order_counts[order_counts['is_weekend'] == True]['product_count'].mean()
        avg_weekday = order_counts[order_counts['is_weekend'] == False]['product_count'].mean()

        return {
            "avg_weekend": avg_weekend,
            "avg_weekday": avg_weekday,
        }
