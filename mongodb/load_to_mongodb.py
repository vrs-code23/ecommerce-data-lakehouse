from pymongo import MongoClient
import pandas as pd
import certifi

MONGO_URI = "mongodb+srv://varsha_admin:YOUR_PASSWORD@cluster0.aozvrql.mongodb.net/?appName=Cluster0"
client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

# client = MongoClient(MONGO_URI)

db = client["ecommerce"]

files = {
    "customers": "data/customers.parquet",
    "orders": "data/orders.parquet",
    "products": "data/products.parquet",
    "inventory": "data/inventory.parquet"
}

for collection_name, file_path in files.items():

    df = pd.read_parquet(file_path)

    db[collection_name].delete_many({})

    db[collection_name].insert_many(
        df.to_dict("records")
    )

    print(f"{collection_name} loaded")

print("MongoDB Load Complete")