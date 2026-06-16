from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# Create Spark Session
spark = SparkSession.builder \
    .appName("Gold Layer Transformation") \
    .getOrCreate()

# Read Silver Layer
silver_df = spark.read.csv(
    "silver_sales_enriched.csv",
    header=True,
    inferSchema=True
)

# ==========================
# 1. Sales By Category
# ==========================

sales_by_category = silver_df.groupBy(
    "category"
).agg(
    sum("order_value").alias("total_sales")
)

# ==========================
# 2. Sales By Country
# ==========================

sales_by_country = silver_df.groupBy(
    "country"
).agg(
    sum("order_value").alias("total_sales")
)

# ==========================
# 3. Top Customers
# ==========================

top_customers = silver_df.groupBy(
    "customer_id",
    "customer_name"
).agg(
    sum("order_value").alias("total_spent")
).orderBy(
    "total_spent",
    ascending=False
)

# ==========================
# 4. Product Performance
# ==========================

product_performance = silver_df.groupBy(
    "product_id",
    "product_name"
).agg(
    sum("quantity").alias("units_sold")
).orderBy(
    "units_sold",
    ascending=False
)

# ==========================
# Preview Results
# ==========================

print("\n===== SALES BY CATEGORY =====")
sales_by_category.show()

print("\n===== SALES BY COUNTRY =====")
sales_by_country.show()

print("\n===== TOP CUSTOMERS =====")
top_customers.show(10)

print("\n===== PRODUCT PERFORMANCE =====")
product_performance.show(10)

# ==========================
# SAVE AS CSV USING PANDAS
# ==========================

sales_by_category.toPandas().to_csv(
    "gold_sales_by_category.csv",
    index=False
)

sales_by_country.toPandas().to_csv(
    "gold_sales_by_country.csv",
    index=False
)

top_customers.toPandas().to_csv(
    "gold_top_customers.csv",
    index=False
)

product_performance.toPandas().to_csv(
    "gold_product_performance.csv",
    index=False
)

print("\n✅ Gold Layer Created Successfully!")

spark.stop()