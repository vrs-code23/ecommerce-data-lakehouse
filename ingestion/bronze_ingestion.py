from pymongo import MongoClient
import pandas as pd
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.config import *

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

collections = {
    "customers": CUSTOMERS_COLLECTION,
    "products": PRODUCTS_COLLECTION,
    "orders": ORDERS_COLLECTION,
    "inventory": INVENTORY_COLLECTION
}

for output_name, collection_name in collections.items():

    print(f"Reading {collection_name}...")

    collection = db[collection_name]

    data = list(
        collection.find({}, {"_id": 0})
    )

    df = pd.DataFrame(data)

    output_path = (
        f"bronze/{output_name}/{output_name}.parquet"
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Saved {output_name} to {output_path}"
    )

print("\nBronze Layer Created Successfully!")
