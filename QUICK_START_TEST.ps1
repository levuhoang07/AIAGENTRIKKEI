param(
    [string]$OutputDir = (Join-Path $PSScriptRoot ("task2-audit-" + (Get-Date -Format "yyyyMMdd-HHmmss-fff")))
)
$ErrorActionPreference = "Stop"
python (Join-Path $PSScriptRoot "03_BENCHMARK_AND_VALIDATION/audit_task2.py") --output $OutputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
