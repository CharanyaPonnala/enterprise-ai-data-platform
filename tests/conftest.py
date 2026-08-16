import sys
from pathlib import Path

# Ensure the project root is importable as a package (`src.*`) regardless of
# pytest's rootdir/import-mode, so tests can `from src...` the same way the
# pipeline code does.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest

from src.ingestion.bronze_ingestion import BRONZE_PATH, TABLES, ingest_csv_to_bronze, spark


@pytest.fixture(scope="session", autouse=True)
def run_bronze_ingestion_once():
    """Runs the real Bronze ingestion pipeline once per test session, so tests
    validate the actual output of src/ingestion/bronze_ingestion.py rather
    than a hand-rolled fixture."""
    for table in TABLES:
        ingest_csv_to_bronze(table)
    yield
    spark.stop()


@pytest.fixture(scope="session")
def bronze_dataframes(run_bronze_ingestion_once):
    return {
        table: spark.read.format("delta").load(f"{BRONZE_PATH}/{table}")
        for table in TABLES
    }
