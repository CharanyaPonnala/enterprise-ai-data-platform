from pathlib import Path

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder
    .appName("bronze-inspection")
    .master("local[*]")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension",
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

bronze_path = Path("data/lakehouse/bronze")

for table in [
    "customers",
    "product_events",
    "support_tickets",
    "invoices",
]:
    path = str(bronze_path / table)
    df = spark.read.format("delta").load(path)

    print(f"\n--- {table} ---")
    print(f"Rows: {df.count()}")
    df.printSchema()
    df.select(
        "_ingested_at",
        "_source_file",
        "_batch_id",
    ).show(3, truncate=False)

spark.stop()
