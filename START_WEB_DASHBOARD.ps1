# -*- coding: utf-8 -*-
# START WEB DASHBOARD LAUNCHER (AI301 ĐỀ 04)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  KHOI DONG NEN TANG WEB DANH GIA THI TRUONG (AI301 DE 04)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$serverScript = Join-Path $PSScriptRoot "02_CORE_PIPELINE_ENGINES\web_server.py"

if (-not (Test-Path $serverScript)) {
    Write-Host "Loi: Khong tim thay script $serverScript" -ForegroundColor Red
    exit 1
}

Write-Host "Dang kiem tra cong mang va khoi dong FastAPI Server..." -ForegroundColor Yellow

# Start browser after 2 seconds
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

python $serverScript

