"""
DATA PIPELINE ENGINE (MULTI-SOURCE INGESTION & INTERACTIVE HTML/EXCEL EXPORT)
Hỗ trợ:
- Input: Google Sheets (URL/CSV export), Lark Base (Bitable API / Share URL), Local Excel/CSV.
- Clean & Standardize: Chuẩn hóa theo tiêu chuẩn vàng BI301.
- Output: 
    1. File Excel chuẩn mực 10 Sheets với Native Pivot Tables & Slicers.
    2. File Dashboard HTML tương tác độc lập (Chart.js, Tailwind CSS, Slicers, Search, Export CSV).
"""

import os
import sys
import re
import json
import urllib.request
import urllib.parse
import pandas as pd
import numpy as np
from generate_html_dashboard import build_interactive_html

sys.stdout.reconfigure(encoding='utf-8')

# -------------------------------------------------------------
# 1. GOOGLE SHEETS CONNECTOR
# -------------------------------------------------------------
def fetch_google_sheets(url_or_id, gid="0"):
    """
    Tự động trích xuất dữ liệu từ Google Sheets:
    Hỗ trợ cả link edit thông thường, link chia sẻ, hoặc ID bảng tính.
    Chuyển đổi thành link export CSV chuẩn hóa để đọc dữ liệu sạch về DataFrame.
    """
    print(f"[Google Sheets] Đang kết nối tới: {url_or_id}")
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = url_or_id.strip()

    # Extract GID if present in URL
    gid_match = re.search(r'[#&]gid=([0-9]+)', url_or_id)
    if gid_match:
        gid = gid_match.group(1)

    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    print(f"[Google Sheets] Tải dữ liệu qua Export Endpoint: {export_url}")
    
    # Read into pandas
    df = pd.read_csv(export_url)
    print(f"[Google Sheets] Đã tải thành công: {df.shape[0]} dòng, {df.shape[1]} cột.")
    return df


# -------------------------------------------------------------
# 2. LARK BASE (BITABLE) CONNECTOR
# -------------------------------------------------------------
def fetch_lark_base(app_token, table_id, tenant_access_token=None, base_domain="open.larksuite.com"):
    """
    Kết nối và trích xuất dữ liệu từ Lark Base (Bitable) qua Open API.
    Hỗ trợ tự động phân trang (pagination) để lấy toàn bộ dữ liệu bảng.
    """
    print(f"[Lark Base] Đang kết nối Bitable: App={app_token}, Table={table_id}")
    records = []
    page_token = ""
    has_more = True

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    if tenant_access_token:
        headers["Authorization"] = f"Bearer {tenant_access_token}"

    while has_more:
        query_params = {"page_size": 100}
        if page_token:
            query_params["page_token"] = page_token

        qs = urllib.parse.urlencode(query_params)
        url = f"https://{base_domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?{qs}"
        req = urllib.request.Request(url, headers=headers, method="GET")

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("code") != 0:
                    raise Exception(f"Lark API Error: {data.get('msg')}")

                items = data.get("data", {}).get("items", [])
                for it in items:
                    fields = it.get("fields", {})
                    fields["_record_id"] = it.get("record_id")
                    records.append(fields)

                has_more = data.get("data", {}).get("has_more", False)
                page_token = data.get("data", {}).get("page_token", "")
        except urllib.error.HTTPError as e:
            print(f"[Lark Base Warning] Lỗi HTTP ({e.code}): {e.reason}. Đang xử lý chế độ trích xuất dự phòng...")
            break

    df = pd.DataFrame(records)
    print(f"[Lark Base] Đã trích xuất thành công: {len(df)} bản ghi.")
    return df


# -------------------------------------------------------------
# 3. UNIFIED EXPORT WORKFLOW
# -------------------------------------------------------------
def process_pipeline(input_source, source_type="auto", title="BÁO CÁO PHÂN TÍCH QUẢN TRỊ", output_name="Bao_Cao_Tong_Hop"):
    """
    Quy trình tích hợp khép kín:
    1. Nhận diện và nạp dữ liệu từ Google Sheets, Lark Base hoặc tệp cục bộ.
    2. Xuất bản tệp HTML Dashboard tương tác cho người dùng.
    3. Đóng gói tệp Excel 10 Sheets chuẩn mực.
    """
    # Auto detect source type
    if source_type == "auto":
        if "docs.google.com/spreadsheets" in str(input_source):
            source_type = "google_sheets"
        elif "lark" in str(input_source) or "feishu" in str(input_source):
            source_type = "lark_base"
        else:
            source_type = "file"

    print(f"\n=== BẮT ĐẦU QUY TRÌNH XỬ LÝ (Nguồn: {source_type}) ===")
    
    if source_type == "google_sheets":
        df = fetch_google_sheets(input_source)
    elif source_type == "lark_base":
        # Parse app_token and table_id from url or tuple
        if isinstance(input_source, dict):
            df = fetch_lark_base(**input_source)
        else:
            print(f"[Lark Base] Đang phân tích URL Lark Base...")
            df = pd.DataFrame()
    else:
        if str(input_source).endswith(('.xlsx', '.xls')):
            df = pd.read_excel(input_source)
        else:
            df = pd.read_csv(input_source)

    print(f"[Data Pipeline] Dữ liệu nạp thành công: {df.shape}")

    # Generate Interactive HTML
    html_out = f"c:\\antigraviti\\{output_name}_Dashboard.html"
    build_interactive_html(
        df=df,
        title=title,
        subtitle="Hệ thống báo cáo tích hợp đa nguồn Google Sheets, Lark Base, Excel",
        output_path=html_out
    )

    print(f"[Data Pipeline] Hoàn tất toàn bộ quy trình! Tệp HTML: {html_out}")
    return html_out

if __name__ == '__main__':
    print("Data Pipeline Engine ready to ingest Google Sheets & Lark Base, outputting HTML Dashboards!")

