from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
RAW_PATH = "data/raw"
BRONZE_PATH = "data/lakehouse/bronze"
builder = (
   SparkSession.builder
   .appName("EnterpriseAIDataPlatformBronzeIngestion")
   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

def ingest_csv_to_bronze(table_name: str):
   input_path = f"{RAW_PATH}/{table_name}.csv"
   output_path = f"{BRONZE_PATH}/{table_name}"
   df = (
       spark.read
       .option("header", True)
       .option("inferSchema", True)
       .csv(input_path)
   )
   (
       df.write
       .format("delta")
       .mode("overwrite")
       .save(output_path)
   )
   print(f"Bronze table created: {table_name}")

if __name__ == "__main__":
   tables = [
       "customers",
       "product_events",
       "support_tickets",
       "invoices"
   ]
   for table in tables:
       ingest_csv_to_bronze(table)
   spark.stop()
