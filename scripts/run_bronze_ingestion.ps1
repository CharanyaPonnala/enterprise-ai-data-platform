<#
.SYNOPSIS
    Runs the bronze ingestion job locally on Windows with the correct Spark/Hadoop environment.

.DESCRIPTION
    PySpark on Windows needs winutils.exe/hadoop.dll (for local filesystem permission checks
    during Delta writes) and a loopback SPARK_LOCAL_IP (to avoid corporate network/VPN sockets
    blocking Spark's driver bind). This script sets those up automatically, then executes
    src\ingestion\bronze_ingestion.py using the project's .venv.

    NOTE ON THIRD-PARTY BINARIES: winutils.exe/hadoop.dll are not published by the Apache Hadoop
    project for Windows, so this script fetches them from the community-maintained
    https://github.com/cdarlint/winutils mirror (hadoop-3.3.5, matching the hadoop-client-api
    version bundled with pyspark). The download only happens once (cached under C:\hadoop\bin)
    and the file hashes are verified against the SHA-256 values pinned below before use; the
    script aborts if they don't match. If you'd rather not fetch third-party binaries at all,
    download/build winutils yourself and place it at C:\hadoop\bin (or point $hadoopHome below
    at your own copy) before running this script.

.EXAMPLE
    .\scripts\run_bronze_ingestion.ps1
#>

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$hadoopHome = "C:\hadoop"
$hadoopBin = Join-Path $hadoopHome "bin"
$winutilsUrl = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/winutils.exe"
$hadoopDllUrl = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/hadoop.dll"
# Pinned SHA-256 checksums for the hadoop-3.3.5 binaries above (cdarlint/winutils mirror).
$winutilsSha256 = "A0CA6E358357C41EF56EBDB02C38E4A4D55DA7CA7A13001678BB2EF7D644ADEA"
$hadoopDllSha256 = "D3DD64AFDC85F2A7EB5345ABF2ECAA744B0A157DE40859313337D47F81EE1C7B"

function Assert-FileHash {
    param([string]$Path, [string]$ExpectedSha256)
    $actual = (Get-FileHash -Path $Path -Algorithm SHA256).Hash
    if ($actual -ne $ExpectedSha256) {
        Remove-Item -Path $Path -Force
        throw "Checksum mismatch for $Path (expected $ExpectedSha256, got $actual). Refusing to use an unverified third-party binary."
    }
}

$winutilsPath = Join-Path $hadoopBin "winutils.exe"
$hadoopDllPath = Join-Path $hadoopBin "hadoop.dll"

# Download winutils.exe / hadoop.dll if not already present, verifying checksums either way.
if (-not (Test-Path $winutilsPath) -or -not (Test-Path $hadoopDllPath)) {
    Write-Output "Hadoop winutils binaries not found. Downloading from third-party mirror (github.com/cdarlint/winutils) to $hadoopBin ..."
    New-Item -ItemType Directory -Force -Path $hadoopBin | Out-Null
    Invoke-WebRequest -Uri $winutilsUrl -OutFile $winutilsPath -UseBasicParsing
    Invoke-WebRequest -Uri $hadoopDllUrl -OutFile $hadoopDllPath -UseBasicParsing
}
Assert-FileHash -Path $winutilsPath -ExpectedSha256 $winutilsSha256
Assert-FileHash -Path $hadoopDllPath -ExpectedSha256 $hadoopDllSha256

$env:HADOOP_HOME = $hadoopHome
$env:PATH = "$hadoopBin;$env:PATH"
$env:SPARK_LOCAL_IP = "127.0.0.1"

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Virtual environment not found at $venvPython. Create it first (e.g. python -m venv .venv; .\.venv\Scripts\pip install -r requirements.txt)."
}

$scriptPath = Join-Path $repoRoot "src\ingestion\bronze_ingestion.py"
& $venvPython $scriptPath
