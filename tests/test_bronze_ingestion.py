from pathlib import Path

import pytest

from src.config.schemas import BRONZE_SCHEMAS
from src.ingestion.bronze_ingestion import BRONZE_PATH, TABLES, batch_id

METADATA_COLUMNS = ("_ingested_at", "_source_file", "_batch_id")


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_table_exists(bronze_dataframes, table_name):
    assert table_name in bronze_dataframes


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_table_has_records(bronze_dataframes, table_name):
    df = bronze_dataframes[table_name]
    assert df.count() > 0


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_table_matches_expected_schema(bronze_dataframes, table_name):
    df = bronze_dataframes[table_name]
    expected_fields = {field.name: field.dataType for field in BRONZE_SCHEMAS[table_name].fields}
    actual_fields = {field.name: field.dataType for field in df.schema.fields}

    for name, expected_type in expected_fields.items():
        assert name in actual_fields, f"Missing expected column '{name}' in table '{table_name}'"
        assert actual_fields[name] == expected_type, (
            f"Column '{name}' in table '{table_name}' has type {actual_fields[name]}, "
            f"expected {expected_type}"
        )


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_table_has_ingestion_metadata_columns(bronze_dataframes, table_name):
    df = bronze_dataframes[table_name]
    for column in METADATA_COLUMNS:
        assert column in df.columns


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_table_batch_id_is_populated(bronze_dataframes, table_name):
    df = bronze_dataframes[table_name]
    distinct_batch_ids = [row["_batch_id"] for row in df.select("_batch_id").distinct().collect()]

    assert distinct_batch_ids == [batch_id]


@pytest.mark.parametrize("table_name", TABLES)
def test_bronze_delta_transaction_log_exists(run_bronze_ingestion_once, table_name):
    delta_log_dir = Path(BRONZE_PATH) / table_name / "_delta_log"

    assert delta_log_dir.is_dir()
    assert any(delta_log_dir.glob("*.json"))
