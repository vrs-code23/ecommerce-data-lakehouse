from faker import Faker
from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.config import *

fake = Faker()

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

customers_col = db[CUSTOMERS_COLLECTION]
products_col = db[PRODUCTS_COLLECTION]
orders_col = db[ORDERS_COLLECTION]
inventory_col = db[INVENTORY_COLLECTION]

# Clear old data
customers_col.delete_many({})
products_col.delete_many({})
orders_col.delete_many({})
inventory_col.delete_many({})

print("Old data deleted...")

# -----------------------------
# Generate Customers
# -----------------------------
customers = []

for _ in range(10000):
    customer = {
        "customer_id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "country": fake.country(),
        "signup_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        ).strftime("%Y-%m-%d")
    }

    customers.append(customer)

customers_col.insert_many(customers)

print(f"{len(customers)} customers inserted")

# -----------------------------
# Generate Products
# -----------------------------
categories = [
    "Electronics",
    "Fashion",
    "Home",
    "Books",
    "Sports"
]

products = []

for i in range(1000):

    product = {
        "product_id": f"P{i+1}",
        "product_name": fake.word().title(),
        "category": random.choice(categories),
        "price": round(random.uniform(100, 5000), 2)
    }

    products.append(product)

products_col.insert_many(products)

print(f"{len(products)} products inserted")

# -----------------------------
# Generate Inventory
# -----------------------------
inventory = []

for product in products:

    item = {
        "product_id": product["product_id"],
        "stock_quantity": random.randint(20, 500),
        "warehouse": random.choice(
            ["Delhi", "Mumbai", "Bangalore"]
        )
    }

    inventory.append(item)

inventory_col.insert_many(inventory)

print(f"{len(inventory)} inventory records inserted")

# -----------------------------
# Generate Orders
# -----------------------------
orders = []

for i in range(50000):

    customer = random.choice(customers)
    product = random.choice(products)

    quantity = random.randint(1, 5)

    order = {
        "order_id": f"O{i+1}",
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "quantity": quantity,
        "price": product["price"],
        "order_value": round(
            quantity * product["price"],
            2
        ),
        "order_date": (
            datetime.now()
            - timedelta(days=random.randint(0, 365))
        ).strftime("%Y-%m-%d")
    }

    orders.append(order)

orders_col.insert_many(orders)

print(f"{len(orders)} orders inserted")

print("\nData generation completed successfully!")