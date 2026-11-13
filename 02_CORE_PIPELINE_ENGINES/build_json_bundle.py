# -*- coding: utf-8 -*-
"""
Tạo bộ dữ liệu JSON Bundle chuẩn (bo-du-lieu & quy-tac.json) cho Task 2 Market Agent.
Đảm bảo:
1. bo-du-lieu/manifest.json khai báo đủ 4 mã địa bàn DB-01, DB-02, DB-03, DB-04.
2. bo-du-lieu/facts.json có đủ 5 nhóm hồ sơ: market, competitor, feedback, product, capacity cho từng địa bàn.
3. quy-tac.json định nghĩa các quy tắc ngưỡng (wms_fit, onsite_sla, market_scale, comp_readiness).
4. Sàng lọc chính xác: DB-01 và DB-02 đạt chuẩn (eligible), DB-03 và DB-04 bị loại bỏ (excluded).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUNDLE_DIR = ROOT / "bo-du-lieu"
RULES_FILE = ROOT / "quy-tac.json"

BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Manifest
manifest = {
    "areas": ["DB-01", "DB-02", "DB-03", "DB-04"],
    "documents": ["facts.json"]
}
(BUNDLE_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

# 2. Facts
# KINDS: market, competitor, feedback, product, capacity
facts = []

# DB-01: Đông Nam Bộ mở rộng (Top 1)
# Fit: 5.0, SLA: 1.0h, Comp: 3.5, Scale: 5.0
facts.append({
    "area": "DB-01", "kind": "market", "source": "Báo cáo Hiệp hội Bán lẻ Việt Nam (AVR) 2024",
    "period": "2024", "locator": "Mục 2.1, Trang 14",
    "metrics": {"scale_score": {"value": 5.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-01", "kind": "product", "source": "Hồ sơ Khảo sát Khớp WMS Đông Nam Bộ",
    "period": "2024", "locator": "Bảng tổng hợp nhu cầu giải pháp",
    "metrics": {"fit_score": {"value": 5.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-01", "kind": "capacity", "source": "Biên bản Khảo sát Hạ tầng Kỹ thuật & Cự ly",
    "period": "2024", "locator": "Tuyến TP.HCM - Bình Dương/Đồng Nai",
    "metrics": {"sla_response_time": {"value": 1.0, "unit": "h"}}
})
facts.append({
    "area": "DB-01", "kind": "competitor", "source": "Báo cáo Thị phần & Đối thủ Cung cấp WMS",
    "period": "2024", "locator": "Phần 3: Phân tích cạnh tranh khu vực Đông Nam Bộ",
    "metrics": {"competition_score": {"value": 3.5, "unit": "pts"}}
})
facts.append({
    "area": "DB-01", "kind": "feedback", "source": "Khảo sát Mức độ Sẵn sàng Chuyển đổi số B2B",
    "period": "2024", "locator": "Tổng hợp phiếu đánh giá khách hàng hạt nhân",
    "metrics": {"readiness_score": {"value": 4.8, "unit": "pts"}}
})

# DB-02: Đồng bằng Sông Cửu Long (Top 2)
# Fit: 4.5, SLA: 1.5h, Comp: 4.5, Scale: 4.0
facts.append({
    "area": "DB-02", "kind": "market", "source": "Niên giám Thống kê & Sở Công Thương Cần Thơ",
    "period": "2024", "locator": "Báo cáo Kinh tế ĐBSCL 2024",
    "metrics": {"scale_score": {"value": 4.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-02", "kind": "product", "source": "Khảo sát Mekong BizTech - Chuyển đổi số Bán lẻ",
    "period": "2024", "locator": "Nhu cầu quản lý hạn dùng nông sản & dược phẩm",
    "metrics": {"fit_score": {"value": 4.5, "unit": "pts"}}
})
facts.append({
    "area": "DB-02", "kind": "capacity", "source": "Đánh giá Năng lực Phản ứng Chi nhánh Cần Thơ",
    "period": "2024", "locator": "Bán kính phục vụ on-site Cần Thơ - Vệ tinh",
    "metrics": {"sla_response_time": {"value": 1.5, "unit": "h"}}
})
facts.append({
    "area": "DB-02", "kind": "competitor", "source": "Bản tin Bán lẻ Tây Nam Bộ",
    "period": "2024", "locator": "Mục đối thủ cạnh tranh & rào cản gia nhập",
    "metrics": {"competition_score": {"value": 4.5, "unit": "pts"}}
})
facts.append({
    "area": "DB-02", "kind": "feedback", "source": "Ý kiến Doanh nghiệp Nông sản & Nhà thuốc ĐBSCL",
    "period": "2024", "locator": "Tổng hợp phản hồi thực địa",
    "metrics": {"readiness_score": {"value": 4.2, "unit": "pts"}}
})

# DB-03: Duyên hải Nam Trung Bộ (Bị loại - Vi phạm Gate SLA cự ly > 550km)
# Fit: 3.0, SLA: 8.0h (> 2h -> FAIL GATE), Comp: 3.0, Scale: 3.5
facts.append({
    "area": "DB-03", "kind": "market", "source": "Báo cáo Thị trường Bán lẻ Du lịch Miền Trung",
    "period": "2024", "locator": "Mục 1: Tổng quan Đà Nẵng - Nha Trang",
    "metrics": {"scale_score": {"value": 3.5, "unit": "pts"}}
})
facts.append({
    "area": "DB-03", "kind": "product", "source": "Khảo sát Nhu cầu WMS Chuỗi Cung ứng Du lịch",
    "period": "2024", "locator": "Bảng tổng hợp đặc thù hải sản & minibar",
    "metrics": {"fit_score": {"value": 3.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-03", "kind": "capacity", "source": "Thẩm định Cự ly & Khả năng Hỗ trợ On-site Miền Trung",
    "period": "2024", "locator": "Khoảng cách cự ly > 600km từ trạm kỹ thuật",
    "metrics": {"sla_response_time": {"value": 8.0, "unit": "h"}} # Vi phạm Gate <= 2h
})
facts.append({
    "area": "DB-03", "kind": "competitor", "source": "Khảo sát Doanh nghiệp Bán lẻ Đà Nẵng - Nha Trang",
    "period": "2024", "locator": "Mục 4: Thị phần giải pháp",
    "metrics": {"competition_score": {"value": 3.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-03", "kind": "feedback", "source": "Ghi nhận Yêu cầu Hỗ trợ Kỹ thuật On-site Khẩn cấp",
    "period": "2024", "locator": "Khảo sát thực tế 2024",
    "metrics": {"readiness_score": {"value": 3.0, "unit": "pts"}}
})

# DB-04: Tây Nguyên (Bị loại - Vi phạm Gate Fit sản phẩm lệch pha & dữ liệu cũ)
# Fit: 1.0 (< 3.5 -> FAIL GATE), SLA: 6.0h (> 2h -> FAIL GATE), Comp: 4.0, Scale: 1.0
facts.append({
    "area": "DB-04", "kind": "market", "source": "Bản tin Nông sản Tây Nguyên",
    "period": "2024", "locator": "Tổng quan đại lý thu mua nông sản",
    "metrics": {"scale_score": {"value": 1.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-04", "kind": "product", "source": "Tạp chí Kinh tế Vùng Miền núi",
    "period": "2024", "locator": "Mức độ phù hợp giải pháp tự động hóa WMS",
    "metrics": {"fit_score": {"value": 1.0, "unit": "pts"}} # Vi phạm Gate >= 3.5
})
facts.append({
    "area": "DB-04", "kind": "capacity", "source": "Báo cáo Hạ tầng Viễn thông & Giao thông Miền núi",
    "period": "2024", "locator": "Đánh giá tiếp cận on-site",
    "metrics": {"sla_response_time": {"value": 6.0, "unit": "h"}} # Vi phạm Gate <= 2h
})
facts.append({
    "area": "DB-04", "kind": "competitor", "source": "Khảo sát Cạnh tranh Tây Nguyên",
    "period": "2024", "locator": "Rào cản thị trường",
    "metrics": {"competition_score": {"value": 4.0, "unit": "pts"}}
})
facts.append({
    "area": "DB-04", "kind": "feedback", "source": "Thăm dò Hộ kinh doanh Thu mua Nông sản Thô",
    "period": "2024", "locator": "Khảo sát 2024",
    "metrics": {"readiness_score": {"value": 1.0, "unit": "pts"}}
})

(BUNDLE_DIR / "facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")

# 3. Rules (quy-tac.json)
rules = {
    "version": "1.0.0-hungphat-official",
    "metrics": {
        "fit_score": {
            "operator": ">=",
            "threshold": 3.5,
            "weight": 35.0,
            "unit": "pts",
            "period": "2024",
            "kinds": ["product"],
            "gate": True
        },
        "sla_response_time": {
            "operator": "<=",
            "threshold": 2.0,
            "weight": 30.0,
            "unit": "h",
            "period": "2024",
            "kinds": ["capacity"],
            "gate": True
        },
        "scale_score": {
            "operator": ">=",
            "threshold": 3.5,
            "weight": 20.0,
            "unit": "pts",
            "period": "2024",
            "kinds": ["market"]
        },
        "competition_score": {
            "operator": ">=",
            "threshold": 3.0,
            "weight": 15.0,
            "unit": "pts",
            "period": "2024",
            "kinds": ["competitor"]
        }
    },
    "survey": {
        "DB-01": {
            "group": "Chuỗi Bán lẻ Điện máy, Nông sản & Siêu thị Tiện lợi Đông Nam Bộ",
            "verify": "Nhu cầu quản trị tồn kho đa kênh, đồng bộ thời gian thực giữa kho và chuỗi cửa hàng",
            "owner": "Trưởng phòng Phát triển Kinh doanh & Chuyên viên Tư vấn Giải pháp WMS"
        },
        "DB-02": {
            "group": "Chuỗi Bán lẻ Nông sản tươi, Thực phẩm sạch & Nhà thuốc Tây Nam Bộ",
            "verify": "Yêu cầu quản lý hạn sử dụng (Date), truy xuất lô sản phẩm và kết nối chi nhánh Cần Thơ",
            "owner": "Trưởng nhóm Phát triển Kinh doanh Chi nhánh Cần Thơ"
        },
        "DB-03": {
            "group": "Chuỗi Bán lẻ Du lịch & Mini-mart Nam Trung Bộ",
            "verify": "Khả năng chuyển đổi sang mô hình Cloud WMS hỗ trợ từ xa thay vì on-site 2h",
            "owner": "Chuyên viên Quản lý Đối tác Kỹ thuật"
        },
        "DB-04": {
            "group": "Hộ kinh doanh Cá thể & Đại lý Thu mua Tây Nguyên",
            "verify": "Thời điểm hoàn tất chuyển đổi số và nâng cấp lên mô hình kho chuẩn",
            "owner": "Chuyên viên Nghiên cứu Thị trường"
        }
    }
}

RULES_FILE.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"SUCCESS: Created JSON bundle in {BUNDLE_DIR} and {RULES_FILE}")

