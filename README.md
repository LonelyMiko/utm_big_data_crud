# Big Data Project

## How to run on local
In order to run this code on local create an `.env` file on project root folder and populate the
DB_CONN variable with `mongodb+srv:...` data from your mongodb cluster. 
Pay attention to the database name inside MongoDB, it must be `instacart_db` and collections names must be: 
1. orders
2. orders_train
3. aisles 
4. departments 
5. products

After this run the `app.py` and access `127.0.0.1:8000/`

Instacart Dataset: https://www.kaggle.com/c/instacart-market-basket-analysis/data