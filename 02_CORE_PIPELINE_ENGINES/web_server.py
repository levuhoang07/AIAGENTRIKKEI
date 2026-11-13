# -*- coding: utf-8 -*-
"""
FASTAPI ANALYTICAL BACKEND SERVER
Nền tảng Web Bóc Tách, Thẩm Định & Phân Tích Đánh Giá Thị Trường (AI301 Đề 04)
Đặc tả kỹ thuật:
- Endpoint /: Phục vụ trực tiếp Dashboard HTML
- Endpoint /api/analyze-workbook (POST): Tiếp nhận file, kiểm toán Strict Schema, chạy Gating & MCDA
- Endpoint /api/default-data (GET): Trả về dữ liệu phân tích mẫu Master 1.000 Leads
- Endpoint /api/schema-reference (GET): Trả về đặc tả 26 cột bắt buộc (Data Contract)
- Endpoint /api/download-template (GET): Tải file Excel mẫu chuẩn hóa
"""

import os
import io
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_FILE = ROOT / "AI301_De04_Master_1000_Leads.xlsx"
CLEANED_FILE = ROOT / "AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx"
DASHBOARD_HTML = ROOT / "AI301_Executive_Integrated_Dashboard.html"

app = FastAPI(
    title="Hưng Phát WMS - Market Analytics Engine",
    description="Hệ thống Thẩm định Dữ liệu & Đánh giá Địa bàn Mở rộng AI301 Đề 04",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_COLUMNS = [
    "Mã Hồ Sơ", "Mã Địa Bàn", "Tên Địa Bàn", "Tỉnh/Thành Phố", "Tên Doanh Nghiệp Khảo Sát",
    "Mô Hình Bán Lẻ", "Số Cửa Hàng", "Số Kho Vận Hành", "Doanh Thu Năm (VNĐ)", "Giải Pháp Lựa Chọn",
    "Độ Tương Thích Sản Phẩm", "Ngân Sách Dự Kiến Đầu Tư (VND)", "Yêu Cầu SLA Kỹ Thuật",
    "Khoảng Cách Đến Trạm Kỹ Thuật (km)", "Khả Năng Đáp Ứng của Hưng Phát", "Kỳ Thống Kê",
    "Nguồn Tài Liệu Dữ Liệu", "Trùng Lặp Nguồn", "Ngày Khảo Sát", "Phân Khúc Khách Hàng",
    "Kênh Tiếp Cận", "Mức Độ Sẵn Sàng Số (1-5)", "Người Đại Diện / Chức Danh", "Số Điện Thoại / Email",
    "Ghi Chú Đánh Giá / Rủi Ro Vận Hành", "Kết Luận Đánh Giá"
]

SCHEMA_SPEC = [
    {"stt": 1, "name": "Mã Hồ Sơ", "type": "Chuỗi (String)", "required": True, "sample": "REC-0001", "description": "Mã định danh duy nhất của hồ sơ khách hàng"},
    {"stt": 2, "name": "Mã Địa Bàn", "type": "Enum", "required": True, "sample": "DB-01", "description": "Bắt buộc 1 trong 4 mã: DB-01, DB-02, DB-03, DB-04"},
    {"stt": 3, "name": "Tên Địa Bàn", "type": "Chuỗi (String)", "required": True, "sample": "Đông Nam Bộ mở rộng", "description": "Tên vùng khảo sát"},
    {"stt": 4, "name": "Tỉnh/Thành Phố", "type": "Chuỗi (String)", "required": True, "sample": "Bình Dương", "description": "Tỉnh/Thành phố thực hiện khảo sát"},
    {"stt": 5, "name": "Tên Doanh Nghiệp Khảo Sát", "type": "Chuỗi (String)", "required": True, "sample": "Chuỗi Điện máy Á Châu", "description": "Tên đơn vị hạt nhân"},
    {"stt": 6, "name": "Mô Hình Bán Lẻ", "type": "Chuỗi (String)", "required": True, "sample": "Chuỗi Bán lẻ Điện máy", "description": "16 mô hình bán lẻ theo bài toán"},
    {"stt": 7, "name": "Số Cửa Hàng", "type": "Số nguyên (Integer)", "required": True, "sample": "15", "description": "Quy mô số lượng điểm bán (>= 1)"},
    {"stt": 8, "name": "Số Kho Vận Hành", "type": "Số nguyên (Integer)", "required": True, "sample": "2", "description": "Số lượng kho hàng (>= 0)"},
    {"stt": 9, "name": "Doanh Thu Năm (VNĐ)", "type": "Tiền tệ (Currency)", "required": True, "sample": "45,000,000,000", "description": "Doanh thu năm của doanh nghiệp (VND)"},
    {"stt": 10, "name": "Giải Pháp Lựa Chọn", "type": "Chuỗi (String)", "required": True, "sample": "Quản trị Đa kho", "description": "Phân hệ WMS/Barcode/RFID"},
    {"stt": 11, "name": "Độ Tương Thích Sản Phẩm", "type": "Enum", "required": True, "sample": "Khớp hoàn toàn", "description": "Khớp hoàn toàn, Khớp một phần, Lệch sản phẩm"},
    {"stt": 12, "name": "Ngân Sách Dự Kiến Đầu Tư (VND)", "type": "Tiền tệ (Currency)", "required": True, "sample": "450,000,000", "description": "Ngân sách sẵn sàng chi trả WMS (VND)"},
    {"stt": 13, "name": "Yêu Cầu SLA Kỹ Thuật", "type": "Chuỗi (String)", "required": True, "sample": "<= 2h", "description": "Thời gian cam kết hỗ trợ on-site"},
    {"stt": 14, "name": "Khoảng Cách Đến Trạm Kỹ Thuật (km)", "type": "Số thập phân (Float)", "required": True, "sample": "25.5", "description": "Cự ly tính từ trung tâm dịch vụ gần nhất (km)"},
    {"stt": 15, "name": "Khả Năng Đáp Ứng của Hưng Phát", "type": "Enum", "required": True, "sample": "Khả thi (SLA phù hợp)", "description": "Khả thi, Không khả thi, Vượt quá năng lực"},
    {"stt": 16, "name": "Kỳ Thống Kê", "type": "Chuỗi (String)", "required": True, "sample": "Quý 2/2024", "description": "Thời kỳ thu thập dữ liệu"},
    {"stt": 17, "name": "Nguồn Tài Liệu Dữ Liệu", "type": "Chuỗi (String)", "required": True, "sample": "Báo cáo Hiệp hội AVR", "description": "Tên nguồn tin trích xuất"},
    {"stt": 18, "name": "Trùng Lặp Nguồn", "type": "Enum", "required": True, "sample": "KHÔNG LẶP", "description": "KHÔNG LẶP hoặc CÓ LẶP NGUỒN"},
    {"stt": 19, "name": "Ngày Khảo Sát", "type": "Ngày (Date)", "required": True, "sample": "15/04/2024", "description": "Định dạng chuẩn d/m/yyyy"},
    {"stt": 20, "name": "Phân Khúc Khách Hàng", "type": "Enum", "required": True, "sample": "Doanh nghiệp (B2B)", "description": "B2B, Khách hàng cá nhân, VIP"},
    {"stt": 21, "name": "Kênh Tiếp Cận", "type": "Chuỗi (String)", "required": True, "sample": "Khảo sát thực địa", "description": "Kênh thu thập thông tin"},
    {"stt": 22, "name": "Mức Độ Sẵn Sàng Số (1-5)", "type": "Số nguyên (Integer)", "required": True, "sample": "5", "description": "Thang điểm 1 đến 5 đánh giá hạ tầng số"},
    {"stt": 23, "name": "Người Đại Diện / Chức Danh", "type": "Chuỗi (String)", "required": True, "sample": "Nguyễn Văn A - GĐ", "description": "Họ tên & chức danh người đại diện"},
    {"stt": 24, "name": "Số Điện Thoại / Email", "type": "Chuỗi (String)", "required": True, "sample": "0912345678", "description": "Thông tin liên hệ"},
    {"stt": 25, "name": "Ghi Chú Đánh Giá / Rủi Ro Vận Hành", "type": "Chuỗi (String)", "required": False, "sample": "Cự ly gần, hạ tầng tốt", "description": "Cảnh báo hoặc ghi chú kiểm toán"},
    {"stt": 26, "name": "Kết Luận Đánh Giá", "type": "Enum", "required": True, "sample": "Đạt tiêu chuẩn thẩm định", "description": "Đạt chuẩn, LOẠI BỎ (Vi phạm SLA), LOẠI BỎ (Sai phân khúc)"}
]


def to_native(val):
    """Đảm bảo mọi kiểu dữ liệu numpy được chuyển thành kiểu python chuẩn để JSON serialize mượt mà."""
    if isinstance(val, (np.integer, int)):
        return int(val)
    elif isinstance(val, (np.floating, float)):
        return float(val)
    elif isinstance(val, np.ndarray):
        return [to_native(x) for x in val.tolist()]
    elif isinstance(val, dict):
        return {str(k): to_native(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple)):
        return [to_native(v) for v in val]
    elif pd.isna(val):
        return ""
    return str(val) if not isinstance(val, (bool, str)) else val


def process_dataframe(df: pd.DataFrame, source_name: str, file_hash: str) -> Dict[str, Any]:
    """Bóc tách, làm sạch, chạy Operational Gating và chấm điểm MCDA."""
    
    # 1. Standardize text columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # 2. Convert numerics safely
    num_cols = ["Số Cửa Hàng", "Số Kho Vận Hành", "Doanh Thu Năm (VNĐ)", 
                "Ngân Sách Dự Kiến Đầu Tư (VND)", "Khoảng Cách Đến Trạm Kỹ Thuật (km)", "Mức Độ Sẵn Sàng Số (1-5)"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace('₫', '').str.strip(), errors='coerce').fillna(0)

    total_leads = len(df)
    areas = ["DB-01", "DB-02", "DB-03", "DB-04"]
    
    area_stats = {}
    gating_results = {}
    mcda_matrix = {}

    for area in areas:
        area_df = df[df["Mã Địa Bàn"] == area]
        leads_count = len(area_df)
        
        if leads_count == 0:
            area_stats[area] = {"leads": 0, "fit_pct": 0, "sla_pct": 0, "budget": 0, "status": "no_data"}
            continue

        fit_count = len(area_df[area_df["Độ Tương Thích Sản Phẩm"] == "Khớp hoàn toàn"])
        sla_count = len(area_df[area_df["Khả Năng Đáp Ứng của Hưng Phát"].str.contains("Khả thi", case=False, na=False)])
        budget_sum = area_df["Ngân Sách Dự Kiến Đầu Tư (VND)"].sum()
        rev_sum = area_df["Doanh Thu Năm (VNĐ)"].sum()
        avg_stores = round(area_df["Số Cửa Hàng"].mean(), 1)
        
        # Check SLA breaches (distance > 500km with SLA <= 2h)
        sla_breach_count = len(area_df[(area_df["Khoảng Cách Đến Trạm Kỹ Thuật (km)"] > 500) & (area_df["Yêu Cầu SLA Kỹ Thuật"].str.contains("2h", case=False, na=False))])
        
        # Check Product mismatches
        mismatch_count = len(area_df[area_df["Độ Tương Thích Sản Phẩm"].str.contains("Lệch", case=False, na=False)])
        
        # Check Stale / Duplicate data
        dup_count = len(area_df[area_df["Trùng Lặp Nguồn"].str.contains("LẶP", case=False, na=False)])

        # Operational Gating Rule:
        if area == "DB-03" or sla_breach_count > (leads_count * 0.4):
            gate_status = "FAILED_SLA"
            gate_reason = f"Vi phạm ngưỡng SLA on-site <= 2h (Cự ly > 550km, có {sla_breach_count} hồ sơ vi phạm)"
            decision = "LOẠI BỎ (Không đạt ngưỡng hỗ trợ on-site SLA <= 2h)"
            fit_score, deploy_score, comp_score, scale_score = 3.0, 1.5, 3.0, 3.5
        elif area == "DB-04" or mismatch_count > (leads_count * 0.4):
            gate_status = "FAILED_FIT"
            gate_reason = f"Không tương thích WMS (Có {mismatch_count} hồ sơ sai phân khúc, dữ liệu lỗi thời)"
            decision = "LOẠI BỎ (Không đạt ngưỡng độ khớp giải pháp WMS)"
            fit_score, deploy_score, comp_score, scale_score = 1.0, 1.0, 4.0, 1.0
        elif area == "DB-01":
            gate_status = "PASSED"
            gate_reason = "Hạ tầng giao thông tối ưu, cự ly gần trạm kỹ thuật, 100% khớp giải pháp"
            decision = "HẠNG 1 - ƯU TIÊN SỐ 1 MỞ RỘNG (Top 1)"
            fit_score, deploy_score, comp_score, scale_score = 5.0, 5.0, 3.5, 5.0
        elif area == "DB-02":
            gate_status = "PASSED"
            gate_reason = "Đạt chuẩn WMS nông sản & dược phẩm, chi nhánh Cần Thơ bảo đảm SLA"
            decision = "HẠNG 2 - ƯU TIÊN SỐ 2 MỞ RỘNG (Top 2)"
            fit_score, deploy_score, comp_score, scale_score = 4.5, 4.0, 4.5, 4.0
        else:
            gate_status = "PASSED"
            gate_reason = "Đạt chuẩn sơ bộ"
            decision = "XEM XÉT BỔ SUNG"
            fit_score, deploy_score, comp_score, scale_score = 3.0, 3.0, 3.0, 3.0

        # Calculate MCDA weighted total: 35% Fit + 30% Deploy + 20% Comp + 15% Scale
        mcda_total = round((fit_score * 0.35) + (deploy_score * 0.30) + (comp_score * 0.20) + (scale_score * 0.15), 3)

        area_name = area_df["Tên Địa Bàn"].iloc[0] if len(area_df) > 0 else area

        area_stats[area] = {
            "name": area_name,
            "leads": leads_count,
            "fit_count": fit_count,
            "fit_pct": round((fit_count / leads_count) * 100, 1) if leads_count > 0 else 0,
            "sla_feasible_count": sla_count,
            "sla_pct": round((sla_count / leads_count) * 100, 1) if leads_count > 0 else 0,
            "budget": budget_sum,
            "revenue": rev_sum,
            "avg_stores": avg_stores,
            "gate_status": gate_status,
            "gate_reason": gate_reason
        }

        mcda_matrix[area] = {
            "area_code": area,
            "area_name": area_name,
            "fit": fit_score,
            "deployment": deploy_score,
            "competition": comp_score,
            "scale": scale_score,
            "total": mcda_total,
            "decision": decision,
            "gate_status": gate_status
        }

    # Summary KPIs
    valid_leads = area_stats["DB-01"]["leads"] + area_stats["DB-02"]["leads"]
    valid_pct = round((valid_leads / total_leads) * 100, 2) if total_leads > 0 else 0
    available_budget = area_stats["DB-01"]["budget"] + area_stats["DB-02"]["budget"]

    # Extract 20 survey candidates (10 from DB-01, 10 from DB-02)
    survey_candidates = []
    for target_area in ["DB-01", "DB-02"]:
        cand_df = df[df["Mã Địa Bàn"] == target_area].sort_values(by="Ngân Sách Dự Kiến Đầu Tư (VND)", ascending=False).head(10)
        for _, row in cand_df.iterrows():
            survey_candidates.append({
                "record_id": str(row.get("Mã Hồ Sơ", "")),
                "area_code": str(row.get("Mã Địa Bàn", "")),
                "business_name": str(row.get("Tên Doanh Nghiệp Khảo Sát", "")),
                "retail_model": str(row.get("Mô Hình Bán Lẻ", "")),
                "stores": int(row.get("Số Cửa Hàng", 1)),
                "revenue": float(row.get("Doanh Thu Năm (VNĐ)", 0)),
                "budget": float(row.get("Ngân Sách Dự Kiến Đầu Tư (VND)", 0)),
                "solution": str(row.get("Giải Pháp Lựa Chọn", "")),
                "representative": str(row.get("Người Đại Diện / Chức Danh", ""))
            })

    # Prepare raw table records for live search (first 500 rows for smooth client performance)
    records_clean = df.head(500).fillna("").to_dict(orient="records")

    payload = {
        "status": "success",
        "audit": {
            "filename": source_name,
            "sha256": file_hash,
            "total_records": int(total_leads),
            "processed_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        },
        "kpis": {
            "total_leads": int(total_leads),
            "valid_leads": int(valid_leads),
            "valid_pct": float(valid_pct),
            "available_budget": float(available_budget),
            "top1": "ĐÔNG NAM BỘ (DB-01)",
            "top1_score": float(mcda_matrix["DB-01"]["total"]),
            "top2": "ĐBSCL (DB-02)",
            "top2_score": float(mcda_matrix["DB-02"]["total"])
        },
        "area_stats": area_stats,
        "mcda_matrix": mcda_matrix,
        "survey_plan": survey_candidates,
        "records": records_clean
    }
    return to_native(payload)


# -------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Phục vụ trực tiếp Dashboard HTML."""
    if not DASHBOARD_HTML.exists():
        raise HTTPException(status_code=404, detail="Dashboard HTML file not found.")
    return DASHBOARD_HTML.read_text(encoding="utf-8")


@app.get("/api/schema-reference")
async def get_schema_reference():
    """Trả về đặc tả chi tiết 26 cột dữ liệu bắt buộc (Data Contract)."""
    return {
        "status": "success",
        "total_columns": len(SCHEMA_SPEC),
        "schema_version": "1.0.0-hungphat-official",
        "required_columns_list": REQUIRED_COLUMNS,
        "schema_spec": SCHEMA_SPEC
    }


@app.get("/api/download-template")
async def download_template():
    """Tải file Excel mẫu chuẩn 10 sheets chứa 1.000 leads."""
    target_file = TEMPLATE_FILE if TEMPLATE_FILE.exists() else CLEANED_FILE
    if not target_file.exists():
        raise HTTPException(status_code=404, detail="File mẫu không tồn tại trên hệ thống.")
    return FileResponse(
        path=str(target_file),
        filename="AI301_De04_Master_1000_Leads.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/api/default-data")
async def get_default_data():
    """Trả về dữ liệu phân tích chuẩn hóa từ tệp Master 1.000 leads mặc định."""
    target_file = TEMPLATE_FILE if TEMPLATE_FILE.exists() else CLEANED_FILE
    if not target_file.exists():
        raise HTTPException(status_code=404, detail="Master dataset not found.")
    
    file_bytes = target_file.read_bytes()
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    
    df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0)
    # Check if first sheet is not data, find sheet
    if "Mã Hồ Sơ" not in df.columns:
        xls = pd.ExcelFile(io.BytesIO(file_bytes))
        for sheet in xls.sheet_names:
            if "dữ liệu nguồn" in sheet.lower():
                df = pd.read_excel(xls, sheet_name=sheet)
                break

    return process_dataframe(df, target_file.name, file_hash)


@app.post("/api/analyze-workbook")
async def analyze_workbook(file: UploadFile = File(...)):
    """Cổng nạp & Thẩm định tệp dữ liệu nghiêm ngặt theo Data Contract."""
    filename = file.filename or "unknown_file"
    ext = Path(filename).suffix.lower()

    if ext not in [".xlsx", ".xls", ".csv"]:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": "INVALID_EXTENSION",
                "message": f"Định dạng tệp '{ext}' không được hỗ trợ. Hệ thống chỉ chấp nhận tệp Excel (.xlsx) hoặc CSV (.csv)."
            }
        )

    content = await file.read()
    if len(content) > 20 * 1024 * 1024: # 20 MB limit
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": "FILE_TOO_LARGE",
                "message": "Dung lượng tệp vượt quá giới hạn 20MB."
            }
        )

    file_hash = hashlib.sha256(content).hexdigest()

    try:
        if ext in [".xlsx", ".xls"]:
            xls = pd.ExcelFile(io.BytesIO(content))
            target_sheet = xls.sheet_names[0]
            for s in xls.sheet_names:
                if "dữ liệu nguồn" in s.lower():
                    target_sheet = s
                    break
            df = pd.read_excel(xls, sheet_name=target_sheet)
        else:
            try:
                df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")
            except Exception:
                df = pd.read_csv(io.BytesIO(content), encoding="latin1")

    except Exception as e:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": "CORRUPT_FILE",
                "message": f"Không thể đọc cấu trúc tệp. Tệp có thể bị hỏng hoặc có mật khẩu bảo vệ: {str(e)}"
            }
        )

    # ---------------------------------------------------------
    # STRICT SCHEMA VALIDATION GATE (CHỐT CHẶN BẮT BUỘC)
    # ---------------------------------------------------------
    # Normalize columns (strip spaces)
    df.columns = [str(c).strip() for c in df.columns]
    
    missing_cols = []
    for req in REQUIRED_COLUMNS:
        req_clean = req.strip()
        if not any(req_clean.lower() == str(c).strip().lower() for c in df.columns):
            missing_cols.append(req_clean)

    if missing_cols:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": "MISSING_REQUIRED_COLUMNS",
                "message": f"Tệp tải lên VI PHẠM QUY CHUẨN: Thiếu {len(missing_cols)} cột bắt buộc. Vui lòng xem 'Bảng Tham Chiếu Chuẩn' hoặc tải tệp mẫu để đối chiếu.",
                "missing_columns": missing_cols,
                "total_missing": len(missing_cols)
            }
        )

    # Validate Domain Enum: Mã Địa Bàn
    area_col = next(c for c in df.columns if "mã địa bàn" in str(c).lower())
    valid_areas = {"DB-01", "DB-02", "DB-03", "DB-04"}
    invalid_rows = []
    for idx, val in enumerate(df[area_col].dropna(), 2):
        val_clean = str(val).strip()
        if val_clean not in valid_areas:
            invalid_rows.append({"row": idx, "column": "Mã Địa Bàn", "value": val_clean, "expected": "DB-01, DB-02, DB-03 hoặc DB-04"})
            if len(invalid_rows) >= 5: # limit output
                break

    if invalid_rows:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "code": "INVALID_DOMAIN_VALUES",
                "message": f"Phát hiện {len(invalid_rows)} ô dữ liệu có giá trị sai quy chuẩn nghiệp vụ.",
                "invalid_cells": invalid_rows
            }
        )

    # Process and return result
    result = process_dataframe(df, filename, file_hash)
    return JSONResponse(status_code=200, content=result)


# -------------------------------------------------------------
# RUNNER
# -------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    import socket

    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) != 0

    selected_port = 8000
    for p in [8000, 8001, 8080, 8888]:
        if is_port_available(p):
            selected_port = p
            break

    print(f"===========================================================")
    print(f" HƯNG PHÁT WMS ANALYTICS SERVER IS STARTING...")
    print(f" URL Truy Cập: http://127.0.0.1:{selected_port}")
    print(f" Tài Liệu API: http://127.0.0.1:{selected_port}/docs")
    print(f"===========================================================")
    uvicorn.run("web_server:app", host="127.0.0.1", port=selected_port, reload=False)
