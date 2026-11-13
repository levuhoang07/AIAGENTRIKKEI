# -*- coding: utf-8 -*-
"""Test FastAPI API Server endpoints & validation logic using Starlette TestClient."""

import io
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from web_server import app, REQUIRED_COLUMNS

client = TestClient(app)

print("=== 1. Test GET / ===")
res = client.get("/")
assert res.status_code == 200
print("PASS: Served Dashboard HTML.")

print("\n=== 2. Test GET /api/schema-reference ===")
res = client.get("/api/schema-reference")
assert res.status_code == 200
data = res.json()
assert data["total_columns"] == 26
print(f"PASS: Schema spec has {data['total_columns']} columns.")

print("\n=== 3. Test GET /api/default-data ===")
res = client.get("/api/default-data")
assert res.status_code == 200
data = res.json()
assert data["kpis"]["total_leads"] == 1000
assert data["kpis"]["top1_score"] == 4.7
assert data["mcda_matrix"]["DB-03"]["gate_status"] == "FAILED_SLA"
assert data["mcda_matrix"]["DB-04"]["gate_status"] == "FAILED_FIT"
print(f"PASS: Default data returned accurately (Top 1 score: {data['kpis']['top1_score']}).")

print("\n=== 4. Test POST /api/analyze-workbook with Valid File ===")
root = Path(__file__).resolve().parents[1]
master_file = root / "AI301_De04_Master_1000_Leads.xlsx"
with open(master_file, "rb") as f:
    res = client.post("/api/analyze-workbook", files={"file": ("test_master.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
assert res.status_code == 200
data = res.json()
assert data["status"] == "success"
print("PASS: Valid workbook parsed and analyzed successfully.")

print("\n=== 5. Test POST /api/analyze-workbook with Missing Columns (Strict Schema Gate) ===")
# Create a dummy bad dataframe missing required columns
bad_df = pd.DataFrame({
    "Mã Hồ Sơ": ["REC-001", "REC-002"],
    "Mã Địa Bàn": ["DB-01", "DB-02"],
    "Tên Doanh Nghiệp Khảo Sát": ["Shop A", "Shop B"]
})
bad_buf = io.BytesIO()
bad_df.to_excel(bad_buf, index=False)
bad_buf.seek(0)

res = client.post("/api/analyze-workbook", files={"file": ("bad_schema.xlsx", bad_buf.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
assert res.status_code == 422
err_data = res.json()
assert err_data["code"] == "MISSING_REQUIRED_COLUMNS"
print(f"PASS: Rejected bad schema with HTTP 422 (Total missing columns caught: {err_data['total_missing']}).")
print("Missing columns sample:", err_data["missing_columns"][:3])

print("\n=== 6. Test POST /api/analyze-workbook with Invalid Domain Value (Mã Địa Bàn) ===")
bad_area_df = pd.read_excel(master_file, sheet_name="Dữ liệu nguồn ").copy()
bad_area_df.loc[0, "Mã Địa Bàn"] = "DB-99" # invalid area
bad_area_buf = io.BytesIO()
bad_area_df.to_excel(bad_area_buf, index=False)
bad_area_buf.seek(0)

res = client.post("/api/analyze-workbook", files={"file": ("bad_area.xlsx", bad_area_buf.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
assert res.status_code == 422
err_data = res.json()
assert err_data["code"] == "INVALID_DOMAIN_VALUES"
print(f"PASS: Caught invalid area code 'DB-99' at row {err_data['invalid_cells'][0]['row']}.")

print("\n>>> ALL 6 API INTEGRATION TESTS PASSED 100%! <<<")
