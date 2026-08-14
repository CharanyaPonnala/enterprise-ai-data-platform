# enterprise-ai-data-platform
Open-source enterprise lakehouse platform with Spark, Delta Lake, Airflow, dbt, data quality, governance, observability, and AI-ready metadata.

## Running bronze ingestion locally (Windows)

PySpark on Windows requires `winutils.exe`/`hadoop.dll` (for local filesystem permission
checks during Delta writes) and, on corporate networks, a loopback `SPARK_LOCAL_IP` (to avoid
VPN/firewall sockets blocking Spark's driver bind). Use the wrapper script below instead of
setting these manually:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python src\ingestion\generate_sample_data.py   # populates data/raw
.\scripts\run_bronze_ingestion.ps1                             # writes data/lakehouse/bronze
```

The script downloads the required Hadoop winutils binaries to `C:\hadoop\bin` on first run
(cached afterward) and sets `HADOOP_HOME`/`SPARK_LOCAL_IP` before invoking
`src\ingestion\bronze_ingestion.py` with the project's `.venv`.
