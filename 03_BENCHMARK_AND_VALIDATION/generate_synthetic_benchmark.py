# -*- coding: utf-8 -*-
"""
SYNTHETIC BENCHMARK DATASET GENERATOR
Generates a realistic 500-row enterprise dataset with 5 injected real-world flaws:
1. SLA Violations (distance > 500km with SLA <= 2h)
2. Product-Segment Mismatch (B2B requesting retail micro-skus)
3. Duplicates & Stale Data
4. Contact & Format Anomalies (spaces, lowercase, bad phones)
5. Regional Revenue Disparity
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

N = 500
regions = ["Miền Bắc", "Miền Trung", "Miền Nam"]
city_map = {
    "Miền Bắc": ["Hà Nội", "Hải Phòng", "Bắc Ninh", "Quảng Ninh", "Hải Dương"],
    "Miền Trung": ["Đà Nẵng", "Huế", "Nha Trang", "Vinh", "Quy Nhơn"],
    "Miền Nam": ["TP. Hồ Chí Minh", "Bình Dương", "Đồng Nai", "Cần Thơ", "Long An"]
}

segments = ["Khách hàng cá nhân", "Thành viên thân thiết (VIP)", "Khách hàng doanh nghiệp (B2B)"]
channels = ["Cửa hàng trực tiếp (In-Store)", "Website / App Online", "Sàn TMĐT (Shopee/Lazada/TikTok)"]
categories = {
    "Thiết bị & Giải pháp": ["Máy quét mã vạch", "Máy in hóa đơn", "Cổng an ninh EAS", "Hệ thống RFID"],
    "Phần mềm & Bản quyền": ["License Cloud Standard", "License Enterprise Pro", "Module Quản lý Date", "Gói Tích hợp ERP"],
    "Vật tư & Tiêu hao": ["Giấy in nhiệt K80", "Cuộn tem nhãn Barcode", "Mực in Ribbon Wax", "Thẻ từ VIP"],
    "Dịch vụ Kỹ thuật": ["Triển khai On-site", "Bảo trì định kỳ", "Đào tạo nhân sự kho", "Tối ưu hóa layout"]
}

records = []
start_date = datetime(2024, 1, 1)

for i in range(1, N + 1):
    reg = random.choice(regions)
    city = random.choice(city_map[reg])
    seg = random.choice(segments)
    chan = random.choice(channels)
    cat = random.choice(list(categories.keys()))
    subcat = random.choice(categories[cat])
    
    qty = random.randint(1, 20) if seg != "Khách hàng doanh nghiệp (B2B)" else random.randint(10, 100)
    price = random.choice([150000, 350000, 850000, 1500000, 4500000, 12000000, 25000000])
    discount_pct = random.choice([0.0, 0.05, 0.1, 0.15, 0.2])
    
    order_date = start_date + timedelta(days=random.randint(0, 365))
    ship_days = random.randint(0, 5)
    satisfaction = random.choice([3, 4, 4, 5, 5, 2, 1])
    is_return = "Có" if satisfaction <= 2 and random.random() < 0.6 else "Không"
    pay_method = random.choice(["Chuyển khoản ngân hàng", "Thẻ tín dụng / Ghi nợ", "Ví MoMo", "Tiền mặt / COD"])
    
    # Base columns
    row = {
        "Mã order": f"ORD-{order_date.strftime('%y%m')}-{i:05d}",
        "Ngày ord": order_date.strftime("%d/%m/%Y"),
        "Tháng ": order_date.strftime("%m/%Y"),
        "Mã KH": f"CUST-{random.randint(1000, 9999)}",
        "Vùng miền ": reg,
        "Thành phố": city,
        "Phân khúc khách hàng ": seg,
        "Kênh bán hàng ": chan,
        "Danh mục nhóm sản phẩm ": cat,
        "Danh mục nhóm sản phẩm con ": subcat,
        "Mã SP": f"SKU-{random.randint(100, 999)}",
        "Tên sản phẩm ": f"{subcat} Chuyên dụng Series-{random.randint(1, 5)}",
        "Số lượng ": qty,
        "Giá niêm yết ": price,
        "Chiết khấu ": discount_pct,
        "Giá vốn hàng bán ": int(price * qty * 0.65),
        "Tgian ship(Day)": ship_days,
        "Hoàn trả": is_return,
        "Mức độ hài lòng ": satisfaction,
        "Phương thức thanh toán ": pay_method
    }
    
    # INJECT REALISTIC ANOMALIES
    # Anomaly 1: SLA distance violation (Ship in 0 days for cities > 500km away from HCMC)
    if reg in ["Miền Bắc", "Miền Trung"] and random.random() < 0.15:
        row["Tgian ship(Day)"] = 0 # Same day / < 2h SLA impossible
        row["Ghi chú SLA"] = "Yêu cầu hỗ trợ kỹ thuật on-site trong 2h (Bất khả thi do cự ly > 600km)"
    else:
        row["Ghi chú SLA"] = "Bình thường"
        
    # Anomaly 2: Whitespace and casing flaws
    if random.random() < 0.08:
        row["Thành phố"] = f"  {city.lower()}  "
        
    # Anomaly 3: Stale 2021 date
    if random.random() < 0.04:
        row["Ngày ord"] = f"{random.randint(1,28)}/{random.randint(1,12)}/2021"
        row["Tháng "] = "2021"

    records.append(row)

# Anomaly 4: Injected duplicate rows
for _ in range(15):
    records.append(dict(records[random.randint(0, 100)]))

df = pd.DataFrame(records)

# Calculate financial columns
gross = df["Số lượng "] * df["Giá niêm yết "]
discount_amt = gross * df["Chiết khấu "]
net_rev = gross - discount_amt
gross_profit = net_rev - df["Giá vốn hàng bán "]
margin = np.where(net_rev > 0, (gross_profit / net_rev) * 100, 0.0)

df["Doanh thu gộp "] = gross
df["Giá chiết khấu "] = discount_amt
df["Doanh thu  thuần "] = net_rev
df["Lợi nhuận gộp"] = gross_profit
df["Biên lợi nhuận gộp "] = margin

out_xlsx = os.path.join(os.path.dirname(__file__), "synthetic_benchmark_dataset.xlsx")
out_csv = os.path.join(os.path.dirname(__file__), "synthetic_benchmark_dataset.csv")

df.to_excel(out_xlsx, index=False)
df.to_csv(out_csv, index=False, encoding="utf-8-sig")

print(f"Generated synthetic benchmark dataset: {len(df)} rows.")
print(f"Saved XLSX: {out_xlsx}")
print(f"Saved CSV:  {out_csv}")