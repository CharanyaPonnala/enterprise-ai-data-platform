from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

CUSTOMERS_SCHEMA = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("customer_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("industry", StringType(), True),
    StructField("company_size", StringType(), True),
    StructField("country", StringType(), True),
    StructField("signup_date", StringType(), True),
    StructField("plan_type", StringType(), True),
    StructField("is_active", BooleanType(), True),
])

PRODUCT_EVENTS_SCHEMA = StructType([
    StructField("event_id", LongType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("event_type", StringType(), True),
    StructField("event_timestamp", StringType(), True),
    StructField("session_duration_seconds", IntegerType(), True),
])

SUPPORT_TICKETS_SCHEMA = StructType([
    StructField("ticket_id", LongType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("priority", StringType(), True),
    StructField("status", StringType(), True),
    StructField("category", StringType(), True),
    StructField("created_at", StringType(), True),
    StructField("resolution_hours", IntegerType(), True),
])

INVOICES_SCHEMA = StructType([
    StructField("invoice_id", LongType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("invoice_date", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("payment_status", StringType(), True),
])

BRONZE_SCHEMAS = {
    "customers": CUSTOMERS_SCHEMA,
    "product_events": PRODUCT_EVENTS_SCHEMA,
    "support_tickets": SUPPORT_TICKETS_SCHEMA,
    "invoices": INVOICES_SCHEMA,
}
