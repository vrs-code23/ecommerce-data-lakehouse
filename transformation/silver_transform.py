from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create Spark Session
spark = SparkSession.builder \
    .appName("Silver Layer Transformation") \
    .getOrCreate()

# Read Bronze Layer Data
customers = spark.read.parquet(
    "bronze/customers/customers.parquet"
)

orders = spark.read.parquet(
    "bronze/orders/orders.parquet"
)

products = spark.read.parquet(
    "bronze/products/products.parquet"
).withColumnRenamed(
    "price",
    "product_price"
)

inventory = spark.read.parquet(
    "bronze/inventory/inventory.parquet"
)

# Join Orders + Customers
silver_df = orders.join(
    customers,
    on="customer_id",
    how="left"
)

# Join Products
silver_df = silver_df.join(
    products,
    on="product_id",
    how="left"
)

# Join Inventory
silver_df = silver_df.join(
    inventory,
    on="product_id",
    how="left"
)

# Check schema before selecting
silver_df.printSchema()

# Select required columns
silver_df = silver_df.select(
    col("order_id"),
    col("customer_id"),
    col("product_id"),

    col("name").alias("customer_name"),
    col("email").alias("customer_email"),

    col("city"),
    col("country"),
    col("signup_date"),

    col("product_name"),
    col("category"),

    col("quantity"),

    col("price"),            # order price
    col("product_price"),    # catalog price

    col("order_value"),
    col("order_date"),

    col("stock_quantity"),
    col("warehouse")
)

# Preview
silver_df.show(10, truncate=False)

# Save Silver Layer
silver_df.coalesce(1).toPandas().to_csv(
    "silver_sales_enriched.csv",
    index=False
)

print("✅ Silver Layer Created Successfully!")

spark.stop()