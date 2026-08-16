import logging
import uuid

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit
from delta import configure_spark_with_delta_pip

from src.config.schemas import BRONZE_SCHEMAS

RAW_PATH = "data/raw"
BRONZE_PATH = "data/lakehouse/bronze"
TABLES = [
   "customers",
   "product_events",
   "support_tickets",
   "invoices",
]

logging.basicConfig(
   level=logging.INFO,
   format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

builder = (
   SparkSession.builder
   .appName("EnterpriseAIDataPlatformBronzeIngestion")
   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# One batch ID per pipeline execution, shared across every table ingested by
# this run so records can be traced back to the run that produced them.
batch_id = str(uuid.uuid4())


def ingest_csv_to_bronze(table_name: str):
   input_path = f"{RAW_PATH}/{table_name}.csv"
   output_path = f"{BRONZE_PATH}/{table_name}"

   logger.info("Starting ingestion for table=%s", table_name)
   try:
      df = (
          spark.read
          .option("header", True)
          .schema(BRONZE_SCHEMAS[table_name])
          .csv(input_path)
      )

      df = (
          df
          .withColumn("_ingested_at", current_timestamp())
          .withColumn("_source_file", input_file_name())
          .withColumn("_batch_id", lit(batch_id))
      )

      row_count = df.count()
      logger.info(
          "Read %s records for table=%s batch_id=%s",
          row_count,
          table_name,
          batch_id,
      )

      (
          df.write
          .format("delta")
          .mode("overwrite")
          .save(output_path)
      )

      logger.info(
          "Successfully wrote Bronze table=%s path=%s",
          table_name,
          output_path,
      )
   except Exception:
      logger.exception(
          "Bronze ingestion failed for table=%s batch_id=%s",
          table_name,
          batch_id,
      )
      raise


if __name__ == "__main__":
   for table in TABLES:
       ingest_csv_to_bronze(table)
   spark.stop()
