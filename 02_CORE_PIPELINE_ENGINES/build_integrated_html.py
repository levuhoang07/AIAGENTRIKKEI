import os
import sys
import json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Read AI301 Cleaned Data
data_file = 'AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx'
if not os.path.exists(data_file):
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx')
df_ai = pd.read_excel(data_file, sheet_name='Dữ liệu nguồn ')

# Convert df to JSON records
records = df_ai.to_dict(orient='records')
for r in records:
    for k, v in r.items():
        if pd.isna(v):
            r[k] = ""
        elif isinstance(v, (np.integer, int)):
            r[k] = int(v)
        elif isinstance(v, (np.floating, float)):
            r[k] = round(float(v), 2)
        else:
            r[k] = str(v)

json_data = json.dumps(records, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Nghiệp Vụ Toàn Diện - Hưng Phát WMS</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background-color: #F8FAFC;
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #CBD5E1;
            border-radius: 4px;
        }}
        .badge-pass {{ background-color: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }}
        .badge-fail {{ background-color: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }}
        .badge-warn {{ background-color: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }}
        .tab-btn.active {{
            border-bottom: 2px solid #2563EB;
            color: #1D4ED8;
            font-weight: 700;
        }}
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- Header Banner -->
    <header class="bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white border-b border-slate-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="bg-blue-600/30 text-blue-300 text-xs font-bold px-2.5 py-0.5 rounded-full border border-blue-500/30">
                            HƯNG PHÁT TECH • WMS SOLUTIONS
                        </span>
                        <span class="text-xs text-slate-400">Chuẩn Hóa Nghiệp Vụ AI301</span>
                    </div>
                    <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight mt-1 text-white">
                        BÁO CÁO THẨM ĐỊNH & CHIẾN LƯỢC MỞ RỘNG THỊ TRƯỜNG TOÀN DIỆN
                    </h1>
                    <p class="text-xs sm:text-sm text-slate-300 mt-0.5">
                        Phân tích 1.000 hồ sơ khảo sát • Khắc phục lỗi Workflow • Chấm điểm MCDA • Kế hoạch thực địa
                    </p>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="window.print()" class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-white/10 hover:bg-white/20 transition-all text-white border border-white/15">
                        <i class="fa-solid fa-print mr-1.5"></i> In Báo Cáo
                    </button>
                    <button onclick="exportToCSV()" class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 transition-all text-white shadow-sm">
                        <i class="fa-solid fa-file-excel mr-1.5"></i> Xuất CSV Sạch
                    </button>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="bg-slate-900/90 border-t border-slate-800 px-4 sm:px-6 lg:px-8">
            <div class="max-w-7xl mx-auto flex space-x-8 text-xs font-medium text-slate-400 overflow-x-auto custom-scrollbar">
                <button onclick="switchTab('tab-dashboard')" id="btn-tab-dashboard" class="tab-btn active py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-chart-pie mr-2"></i> 1. Dashboard Quản Trị & Slicers
                </button>
                <button onclick="switchTab('tab-management')" id="btn-tab-management" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-briefcase mr-2"></i> 2. Phân Tích Nghiệp Vụ, Workflow Lỗi & Giải Pháp
                </button>
                <button onclick="switchTab('tab-mcda')" id="btn-tab-mcda" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-ranking-star mr-2"></i> 3. Ma Trận Chấm Điểm MCDA & Top 2
                </button>
                <button onclick="switchTab('tab-survey')" id="btn-tab-survey" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-clipboard-check mr-2"></i> 4. Kế Hoạch Khảo Sát 20 Chuỗi Hạt Nhân
                </button>
                <button onclick="switchTab('tab-data')" id="btn-tab-data" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-database mr-2"></i> 5. Bảng Dữ Liệu Chi Tiết (1.000 Leads)
                </button>
            </div>
        </div>
    </header>

    <!-- Main Body Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- ========================================================= -->
        <!-- TAB 1: EXECUTIVE DASHBOARD -->
        <!-- ========================================================= -->
        <div id="tab-dashboard" class="tab-content space-y-6">
            <!-- KPI Cards -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Tổng Leads Đầu Vào</p>
                    <p class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">1,000</p>
                    <p class="text-xs text-slate-500 mt-1 flex items-center">
                        <i class="fa-solid fa-location-dot mr-1 text-blue-500"></i> Phân bổ trên 4 địa bàn
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-emerald-600 uppercase tracking-wider">Tỷ Lệ Đạt Chuẩn Gating</p>
                    <p class="text-2xl sm:text-3xl font-extrabold text-emerald-600 mt-1">59.80%</p>
                    <p class="text-xs text-slate-500 mt-1">
                        598 / 1,000 hồ sơ vượt qua 2 chốt chặn
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-blue-600 uppercase tracking-wider">Ngân Sách Khả Dụng Thực Tế</p>
                    <p class="text-2xl sm:text-3xl font-extrabold text-blue-700 mt-1">147.57 Tỷ ₫</p>
                    <p class="text-xs text-slate-500 mt-1">
                        Sẵn sàng chi trả giải pháp WMS
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-indigo-600 uppercase tracking-wider">Chiến Lược Mở Rộng</p>
                    <p class="text-xl font-extrabold text-indigo-700 mt-1">DB-01 & DB-02</p>
                    <p class="text-xs text-slate-500 mt-1">
                        Đông Nam Bộ (#1) & ĐBSCL (#2)
                    </p>
                </div>
            </div>

            <!-- Interactive Slicers Bar -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
                <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    <div class="flex items-center space-x-2 text-slate-800 font-bold text-sm">
                        <i class="fa-solid fa-sliders text-indigo-600"></i>
                        <span>Bộ Lọc Đa Chiều (Slicers):</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1 lg:max-w-3xl">
                        <div>
                            <select id="slicer-region" onchange="applySlicers()" class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg p-2 outline-none">
                                <option value="">Tất cả địa bàn (4 Địa bàn)</option>
                                <option value="Đông Nam Bộ mở rộng (Bình Dương - Đồng Nai - BRVT)">Đông Nam Bộ (DB-01)</option>
                                <option value="Đồng bằng Sông Cửu Long (Cần Thơ - Tiền Giang - An Giang)">ĐBSCL (DB-02)</option>
                                <option value="Duyên hải Nam Trung Bộ (Đà Nẵng - Quảng Nam - Khánh Hòa)">Nam Trung Bộ (DB-03)</option>
                                <option value="Tây Nguyên (Đắk Lắk - Gia Lai - Lâm Đồng)">Tây Nguyên (DB-04)</option>
                            </select>
                        </div>
                        <div>
                            <select id="slicer-status" onchange="applySlicers()" class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg p-2 outline-none">
                                <option value="">Tất cả trạng thái thẩm định</option>
                                <option value="ĐẠT TIÊU CHUẨN (PASS_ALL: Đủ điều kiện chấm điểm mở rộng)">ĐẠT TIÊU CHUẨN (PASS_ALL)</option>
                                <option value="LOẠI BỎ (FAIL_KNOCKOUT_SUPPORT: Yêu cầu hỗ trợ tại chỗ vượt quá năng lực Hưng Phát)">LOẠI BỎ - Hỗ trợ SLA</option>
                                <option value="LOẠI BỎ (FAIL_KNOCKOUT_PRODUCT: Khách hàng là đại lý nông sản thô, không khớp WMS)">LOẠI BỎ - Lệch WMS</option>
                            </select>
                        </div>
                        <div>
                            <input type="text" id="slicer-search" oninput="applySlicers()" placeholder="Tìm tên chuỗi, người đại diện, số đt..." class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg p-2 outline-none">
                        </div>
                    </div>
                    <div>
                        <button onclick="resetSlicers()" class="text-xs text-indigo-600 font-semibold hover:underline">
                            Đặt lại
                        </button>
                    </div>
                </div>
            </div>

            <!-- Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <h3 class="text-sm font-bold text-slate-900 mb-3 flex items-center">
                        <i class="fa-solid fa-chart-column mr-2 text-blue-600"></i>
                        Quy Mô Ngân Sách Dự Kiến Theo Địa Bàn (VNĐ)
                    </h3>
                    <div class="h-64"><canvas id="chart-budget"></canvas></div>
                </div>
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <h3 class="text-sm font-bold text-slate-900 mb-3 flex items-center">
                        <i class="fa-solid fa-chart-pie mr-2 text-indigo-600"></i>
                        Cơ Cấu Tỷ Lệ Sàng Lọc Gating Filter
                    </h3>
                    <div class="h-64"><canvas id="chart-gating"></canvas></div>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 2: MANAGEMENT REPORT & WORKFLOW ANALYSIS (YÊU CẦU FILE WORD) -->
        <!-- ========================================================= -->
        <div id="tab-management" class="tab-content hidden space-y-6">
            
            <!-- Section 1: Hồ sơ công ty -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="border-b border-slate-200 pb-4 mb-4">
                    <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">Phần I: Hồ Sơ Doanh Nghiệp & Thị Trường</span>
                    <h2 class="text-lg font-bold text-slate-900 mt-1">CÔNG TY HƯNG PHÁT LÀ CÔNG TY GÌ? BUÔN BÁN GÌ? KHÁCH HÀNG LÀ AI?</h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-700 leading-relaxed">
                    <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                        <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center text-indigo-700">
                            <i class="fa-solid fa-building mr-2"></i> 1. Hồ Sơ Công Ty
                        </h4>
                        <p><strong>Công ty Hưng Phát</strong> là doanh nghiệp công nghệ giải pháp phần mềm tại TP.HCM, chuyên thiết kế và cung cấp hệ thống <strong>Quản lý kho hàng thông minh (Warehouse Management System - WMS)</strong>.</p>
                        <p class="mt-2">Đội ngũ triển khai có trình độ kỹ thuật cao nhưng định biên có hạn, trụ sở chính tại TP.HCM, bán kính hỗ trợ kỹ thuật tại chỗ (On-site SLA) tối ưu trong phạm vi &le; 100km.</p>
                    </div>
                    <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                        <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center text-blue-700">
                            <i class="fa-solid fa-box mr-2"></i> 2. Sản Phẩm / Dịch Vụ
                        </h4>
                        <p>Cung cấp 3 gói giải pháp WMS chuyên biệt:</p>
                        <ul class="list-disc list-inside mt-1.5 space-y-1">
                            <li><strong>Hưng Phát WMS Cloud Standard:</strong> Gói đám mây tiêu chuẩn cho chuỗi bán lẻ.</li>
                            <li><strong>Hưng Phát WMS Pro Enterprise:</strong> Gói doanh nghiệp cao cấp cho chuỗi đa kho lớn.</li>
                            <li><strong>WMS Quản lý Hạn/Date:</strong> Gói đặc thù cho Thực phẩm, Nông sản sạch & Dược phẩm.</li>
                        </ul>
                    </div>
                    <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                        <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center text-emerald-700">
                            <i class="fa-solid fa-users mr-2"></i> 3. Khách Hàng Mục Tiêu
                        </h4>
                        <p>Chuỗi bán lẻ hiện đại (Siêu thị mini, Chuỗi thời trang, Điện máy gia dụng, Chuỗi F&B, Chuỗi nhà thuốc tây) có từ <strong>5 – 50 cửa hàng</strong> và vận hành từ <strong>2 – 6 kho hàng</strong>.</p>
                        <p class="mt-2"><em>Không phục vụ:</em> Đại lý thu mua nông sản thô sơ (cà phê, tiêu) hoặc hộ kinh doanh tạp hóa chỉ có nhu cầu sổ sách/Excel.</p>
                    </div>
                </div>
            </div>

            <!-- Section 2: Vấn đề & Nguyên nhân & Workflow Lỗi -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="border-b border-slate-200 pb-4 mb-4">
                    <span class="text-xs font-bold text-rose-600 uppercase tracking-wider">Phần II: Vấn Đề Gặp Phải & Phân Tích Workflow Bị Lỗi</span>
                    <h2 class="text-lg font-bold text-slate-900 mt-1">NGUYÊN NHÂN GỐC RỄ & PHÂN TÍCH QUY TRÌNH LỖI (WORKFLOW AS-IS)</h2>
                </div>

                <!-- 7 Vấn đề cốt lõi -->
                <div class="mb-6">
                    <h3 class="text-sm font-bold text-slate-900 mb-3">7 Vấn Đề Nghiệp Vụ Cốt Lõi Được Bóc Tách Từ 1.000 Leads:</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div class="p-3 bg-rose-50 rounded-lg border border-rose-200 text-rose-900">
                            <strong>1. Giới hạn nghiêm ngặt về năng lực thực thi:</strong> Đội kỹ thuật chỉ đủ nguồn lực phục vụ duy nhất 1 đợt mở rộng, không thể dàn trải sang cả 4 địa bàn.
                        </div>
                        <div class="p-3 bg-rose-50 rounded-lg border border-rose-200 text-rose-900">
                            <strong>2. Quy trình làm việc tự phát, phân tán:</strong> Nhân viên tự đọc báo cáo thị trường, tự gom thông tin đối thủ và tự ghép leads mà không có chuẩn mực chung.
                        </div>
                        <div class="p-3 bg-amber-50 rounded-lg border border-amber-200 text-amber-900">
                            <strong>3. Dữ liệu không đồng nhất về thời gian:</strong> Lẫn lộn số liệu cũ năm 2021 (200 leads Tây Nguyên), 9T/2023 (134 leads Nam Trung Bộ) với số liệu 2024.
                        </div>
                        <div class="p-3 bg-amber-50 rounded-lg border border-amber-200 text-amber-900">
                            <strong>4. Dữ liệu trùng lặp và thiếu tính độc lập:</strong> 200 bản ghi tại Tây Nguyên bị sao chép từ cùng một nguồn cũ mà không được thanh lọc.
                        </div>
                        <div class="p-3 bg-indigo-50 rounded-lg border border-indigo-200 text-indigo-900">
                            <strong>5. Đánh giá sai lệch trọng tâm thị trường:</strong> Nhân viên chỉ nhìn vào doanh thu lớn mà bỏ qua việc khách hàng có khớp với tính năng WMS hay không.
                        </div>
                        <div class="p-3 bg-indigo-50 rounded-lg border border-indigo-200 text-indigo-900">
                            <strong>6. Bất cân xứng giữa kỳ vọng khách và khả năng cung ứng:</strong> 202 chuỗi tại Nam Trung Bộ đòi On-site SLA &le; 2h và trực 24/7, vượt trần công suất kỹ thuật Hưng Phát.
                        </div>
                        <div class="p-3 bg-slate-100 rounded-lg border border-slate-300 text-slate-900 col-span-1 md:col-span-2">
                            <strong>7. Thiếu tính minh bạch và khả năng kiểm chứng:</strong> Toàn bộ hồ sơ khảo sát thiếu mã truy vết (Audit Trail), không thể kiểm tra chéo nguồn gốc số liệu.
                        </div>
                    </div>
                </div>

                <!-- So sánh Workflow Lỗi vs Workflow Chuẩn Hóa -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-200 text-xs">
                    <div>
                        <h4 class="font-bold text-rose-700 text-sm mb-2 flex items-center">
                            <i class="fa-solid fa-triangle-exclamation mr-2"></i> WORKFLOW LỖI HIỆN TẠI (AS-IS) - AI LÀM?
                        </h4>
                        <div class="space-y-2 border-l-2 border-rose-300 pl-4 py-1 text-slate-600">
                            <p><strong>• Tác nhân (Ai làm?):</strong> Con người thực hiện 100% thủ công (Nhân viên Nghiên cứu thị trường và Chuyên viên Kinh doanh).</p>
                            <p><strong>• Cách làm:</strong> Nhân viên tự tìm kiếm báo cáo trên mạng, cào dữ liệu thô, nhập tự do vào Excel mà không có quy chuẩn xác thực.</p>
                            <p><strong>• Điểm đứt gãy:</strong> Không có bước sàng lọc kỹ thuật (Gating Filter); trình hồ sơ trực tiếp lên Ban Giám Đốc chỉ dựa trên con số doanh thu ảo.</p>
                            <p><strong>• Hậu quả:</strong> Gây lãng phí chi phí đi công tác thực địa, chào hàng sai đối tượng (đại lý cà phê) và đối mặt rủi ro phạt hợp đồng SLA do không tới kịp trong 2h.</p>
                        </div>
                    </div>

                    <div>
                        <h4 class="font-bold text-emerald-700 text-sm mb-2 flex items-center">
                            <i class="fa-solid fa-circle-check mr-2"></i> WORKFLOW CHUẨN HÓA MỚI (TO-BE) - 4 BƯỚC
                        </h4>
                        <div class="space-y-2 border-l-2 border-emerald-400 pl-4 py-1 text-slate-700">
                            <p><strong>[Bước 1: Làm sạch & Chuẩn hóa]:</strong> Khử trùng lặp (Deduplication), quy chuẩn mốc thời gian 2024 (Time Alignment), gắn mã định danh REC-xxxx.</p>
                            <p><strong>[Bước 2: Gating Filter]:</strong> Máy & Đội kỹ thuật chạy 2 chốt chặn loại bỏ hồ sơ lệch WMS và vượt ngưỡng On-site SLA &le; 2h.</p>
                            <p><strong>[Bước 3: Chấm điểm MCDA]:</strong> Tính toán điểm số trọng số khoa học (35% Khớp WMS, 30% Khả thi, 20% Cạnh tranh, 15% Quy mô).</p>
                            <p><strong>[Bước 4: Báo cáo & Thực địa]:</strong> Lập tờ trình Ban Giám Đốc phê duyệt mở rộng Top 2 và tiến hành phỏng vấn sâu 20 chuỗi hạt nhân.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section 3: Đề xuất giải pháp -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="border-b border-slate-200 pb-4 mb-4">
                    <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">Phần III: Đề Xuất Giải Pháp Quản Trị</span>
                    <h2 class="text-lg font-bold text-slate-900 mt-1">GIẢI PHÁP ƯU TIÊN (TỐI ƯU NGUỒN LỰC) & GIẢI PHÁP DÀI HẠN</h2>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                    <div class="bg-blue-50/70 p-4 rounded-xl border border-blue-200">
                        <span class="bg-blue-600 text-white font-bold text-[10px] px-2 py-0.5 rounded uppercase">Ưu Tiên Số 1 - Thực Thi Ngay</span>
                        <h4 class="font-bold text-slate-900 text-sm mt-2 mb-2">Tập Trung Toàn Lực Mở Rộng 2 Địa Bàn Hạt Nhân (DB-01 & DB-02)</h4>
                        <ul class="space-y-2 text-slate-700">
                            <li><strong>• Cực tăng trưởng số 1 - Đông Nam Bộ (DB-01):</strong> Đạt điểm MCDA 4.70/5. Tận dụng cự ly < 100km từ TP.HCM để cam kết On-site SLA 3-4h. Khai thác ngay 320 chuỗi với tổng ngân sách 93.18 tỷ ₫.</li>
                            <li><strong>• Cực tăng trưởng số 2 - ĐBSCL (DB-02):</strong> Đạt điểm MCDA 4.28/5. Cạnh tranh thấp, áp dụng mô hình Go-live On-site 2-3 ngày đầu, sau đó chuyển sang Remote SLA 30 phút. Khai thác 250 chuỗi thực phẩm sạch & nhà thuốc với ngân sách 49.01 tỷ ₫.</li>
                            <li><strong>• Cắt giảm ngay chi phí lãng phí:</strong> Dừng toàn bộ hoạt động tiếp thị và khảo sát tại DB-03 và DB-04, tiết kiệm 100% ngân sách công tác vô ích.</li>
                        </ul>
                    </div>

                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <span class="bg-slate-700 text-white font-bold text-[10px] px-2 py-0.5 rounded uppercase">Giải Pháp Dài Hạn - Chuẩn Hóa Hệ Thống</span>
                        <h4 class="font-bold text-slate-900 text-sm mt-2 mb-2">Nâng Cấp Năng Lực Cung Ứng & Chuyển Đổi Số Quy Trình</h4>
                        <ul class="space-y-2 text-slate-700">
                            <li><strong>• Thiết lập Hub Kỹ thuật Vùng tại Đà Nẵng:</strong> Khi mở rộng giai đoạn 2, thành lập trạm kỹ thuật tại chỗ trước khi nhận khách hàng đòi hỏi SLA &le; 2h tại Duyên hải Miền Trung.</li>
                            <li><strong>• Tự động hóa Pipeline Đa Nguồn:</strong> Tích hợp tự động nạp dữ liệu từ Google Sheets và Lark Base vào quy trình kiểm tra lỗi QA Flags tự động (như module đã thiết lập).</li>
                            <li><strong>• Gói giải pháp WMS Nông nghiệp tinh gọn:</strong> Nghiên cứu phân hệ WMS chuyên biệt cho nông sản xuất khẩu trước khi quay lại thị trường Tây Nguyên.</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>

        <!-- ========================================================= -->
        <!-- TAB 3: MA TRẬN CHẤM ĐIỂM MCDA -->
        <!-- ========================================================= -->
        <div id="tab-mcda" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="border-b border-slate-200 pb-4 mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                        <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">Bước 3: Đánh Giá Đa Tiêu Chí</span>
                        <h2 class="text-lg font-bold text-slate-900 mt-0.5">MA TRẬN CHẤM ĐIỂM MCDA (MULTI-CRITERIA DECISION ANALYSIS)</h2>
                    </div>
                    <div class="text-xs text-slate-500 font-medium">Thang điểm: 1.0 đến 5.0</div>
                </div>

                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-white font-bold uppercase text-[11px]">
                                <th class="p-3 border border-slate-800">Mã ĐB</th>
                                <th class="p-3 border border-slate-800">Tên Địa Bàn Khảo Sát</th>
                                <th class="p-3 border border-slate-800 text-center">Độ Khớp WMS (35%)</th>
                                <th class="p-3 border border-slate-800 text-center">Khả Thi Triển Khai (30%)</th>
                                <th class="p-3 border border-slate-800 text-center">Cạnh Tranh (20%)</th>
                                <th class="p-3 border border-slate-800 text-center">Quy Mô Chuỗi (15%)</th>
                                <th class="p-3 border border-slate-800 text-center font-extrabold text-yellow-300">Tổng Điểm MCDA</th>
                                <th class="p-3 border border-slate-800">Quyết Định Chiến Lược</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200">
                            <tr class="bg-emerald-50/70 font-semibold text-slate-900">
                                <td class="p-3 border text-center font-bold text-emerald-800">DB-01</td>
                                <td class="p-3 border font-bold">Đông Nam Bộ mở rộng (Bình Dương - Đồng Nai - BRVT)</td>
                                <td class="p-3 border text-center">5.0</td>
                                <td class="p-3 border text-center">5.0</td>
                                <td class="p-3 border text-center">3.5</td>
                                <td class="p-3 border text-center">5.0</td>
                                <td class="p-3 border text-center font-extrabold text-emerald-800 text-sm">4.70</td>
                                <td class="p-3 border text-emerald-700 font-bold">HẠNG 1 (TOP 1) - Ưu tiên số 1 mở rộng ngay</td>
                            </tr>
                            <tr class="bg-blue-50/70 font-semibold text-slate-900">
                                <td class="p-3 border text-center font-bold text-blue-800">DB-02</td>
                                <td class="p-3 border font-bold">Đồng bằng Sông Cửu Long (Cần Thơ - Tiền Giang - An Giang)</td>
                                <td class="p-3 border text-center">4.5</td>
                                <td class="p-3 border text-center">4.0</td>
                                <td class="p-3 border text-center">4.5</td>
                                <td class="p-3 border text-center">4.0</td>
                                <td class="p-3 border text-center font-extrabold text-blue-800 text-sm">4.28</td>
                                <td class="p-3 border text-blue-700 font-bold">HẠNG 2 (TOP 2) - Ưu tiên số 2 mô hình Hybrid</td>
                            </tr>
                            <tr class="bg-rose-50/50 text-slate-600">
                                <td class="p-3 border text-center font-bold text-rose-700">DB-03</td>
                                <td class="p-3 border">Duyên hải Nam Trung Bộ (Đà Nẵng - Quảng Nam - Khánh Hòa)</td>
                                <td class="p-3 border text-center">3.0</td>
                                <td class="p-3 border text-center">1.5</td>
                                <td class="p-3 border text-center">3.0</td>
                                <td class="p-3 border text-center">3.5</td>
                                <td class="p-3 border text-center font-bold text-rose-700">2.53</td>
                                <td class="p-3 border text-rose-600">LOẠI BỎ - 87.8% vi phạm ngưỡng On-site SLA &le; 2h</td>
                            </tr>
                            <tr class="bg-slate-100 text-slate-500">
                                <td class="p-3 border text-center font-bold">DB-04</td>
                                <td class="p-3 border">Tây Nguyên (Đắk Lắk - Gia Lai - Lâm Đồng)</td>
                                <td class="p-3 border text-center">1.0</td>
                                <td class="p-3 border text-center">1.0</td>
                                <td class="p-3 border text-center">4.0</td>
                                <td class="p-3 border text-center">1.0</td>
                                <td class="p-3 border text-center font-bold">1.60</td>
                                <td class="p-3 border text-rose-600">LOẠI BỎ - 100% lệch WMS & 100% lặp dữ liệu cũ 2021</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="mt-4 p-4 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-600">
                    <p class="font-bold text-slate-800 mb-1">Công thức tính điểm trọng số:</p>
                    <p class="font-mono bg-white p-2 rounded border border-slate-300 inline-block">
                        Điểm MCDA = (Điểm Khớp WMS &times; 35%) + (Điểm Khả Thi &times; 30%) + (Điểm Cạnh Tranh &times; 20%) + (Điểm Quy Mô &times; 15%)
                    </p>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 4: KẾ HOẠCH KHẢO SÁT 20 CHUỖI HẠT NHÂN -->
        <!-- ========================================================= -->
        <div id="tab-survey" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="border-b border-slate-200 pb-4 mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                        <span class="text-xs font-bold text-emerald-600 uppercase tracking-wider">Bước 4: Thực Địa Thị Trường</span>
                        <h2 class="text-lg font-bold text-slate-900 mt-0.5">DANH SÁCH 20 CHUỖI BÁN LẺ HẠT NHÂN ĐƯỢC CHỌN KHẢO SÁT CHUYÊN SÂU</h2>
                    </div>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">
                        Top 10 DB-01 & Top 10 DB-02
                    </span>
                </div>

                <p class="text-xs text-slate-600 mb-4">
                    Các doanh nghiệp được tuyển chọn đại diện có quy mô doanh thu lớn nhất, hệ thống kho vận hành hoàn chỉnh và đã vượt qua 100% các tiêu chí Gating Filter:
                </p>

                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-white font-bold uppercase text-[11px]">
                                <th class="p-3 border border-slate-800">Mã HS</th>
                                <th class="p-3 border border-slate-800">Mã ĐB</th>
                                <th class="p-3 border border-slate-800">Tên Doanh Nghiệp Khảo Sát</th>
                                <th class="p-3 border border-slate-800">Mô Hình Bán Lẻ</th>
                                <th class="p-3 border border-slate-800 text-right">Số Cửa Hàng</th>
                                <th class="p-3 border border-slate-800 text-right">Doanh Thu Năm (VNĐ)</th>
                                <th class="p-3 border border-slate-800">Giải Pháp Lựa Chọn</th>
                                <th class="p-3 border border-slate-800">Người Đại Diện & Chức Danh</th>
                            </tr>
                        </thead>
                        <tbody id="survey-table-body" class="divide-y divide-slate-200">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 5: BẢNG DỮ LIỆU CHI TIẾT (1.000 LEADS) -->
        <!-- ========================================================= -->
        <div id="tab-data" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <div class="p-4 sm:p-5 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div>
                        <h2 class="text-base font-bold text-slate-900 flex items-center">
                            <i class="fa-solid fa-table text-indigo-600 mr-2"></i>
                            Toàn Bộ 1.000 Hồ Sơ Khảo Sát Đã Qua Làm Sạch (Table1)
                        </h2>
                        <p class="text-xs text-slate-500 mt-0.5">Hiển thị <span id="showing-count" class="font-bold text-indigo-600">0</span> / 1,000 bản ghi</p>
                    </div>
                    <div class="flex items-center space-x-2 text-xs">
                        <span class="text-slate-500">Số dòng/trang:</span>
                        <select id="page-size" onchange="changePageSize()" class="bg-slate-50 border border-slate-300 rounded px-2.5 py-1 text-xs outline-none">
                            <option value="15">15</option>
                            <option value="25" selected>25</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold uppercase text-[11px] border-b border-slate-200">
                                <th class="p-3 whitespace-nowrap">Mã HS</th>
                                <th class="p-3 whitespace-nowrap">Mã ĐB</th>
                                <th class="p-3 whitespace-nowrap">Tên Doanh Nghiệp</th>
                                <th class="p-3 whitespace-nowrap">Mô Hình Bán Lẻ</th>
                                <th class="p-3 whitespace-nowrap text-right">Số Shop</th>
                                <th class="p-3 whitespace-nowrap text-right">Ngân Sách (VNĐ)</th>
                                <th class="p-3 whitespace-nowrap">Giải Pháp WMS</th>
                                <th class="p-3 whitespace-nowrap">Kết Luận Đánh Giá</th>
                            </tr>
                        </thead>
                        <tbody id="master-table-body" class="divide-y divide-slate-100">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="p-4 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-xs text-slate-600">
                    <div id="pagination-info">Trang 1 / 1</div>
                    <div class="flex items-center space-x-1.5">
                        <button onclick="prevPage()" id="btn-prev" class="px-3 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 font-semibold disabled:opacity-40">
                            Trước
                        </button>
                        <button onclick="nextPage()" id="btn-next" class="px-3 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 font-semibold disabled:opacity-40">
                            Sau
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        Báo cáo Tích Hợp Nghiệp Vụ Quản Trị • Hệ Thống Chuẩn Hóa BI301 • Hỗ Trợ Đa Nguồn Google Sheets, Lark Base, Excel.
    </footer>

    <!-- Logic Script -->
    <script>
        const allRecords = {json_data};
        let filteredRecords = [...allRecords];
        let currentPage = 1;
        let pageSize = 25;
        let chartBudget = null;
        let chartGating = null;

        window.addEventListener('DOMContentLoaded', () => {{
            renderSurveyTable();
            applySlicers();
        }});

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).classList.add('active');

            if (tabId === 'tab-dashboard') {{
                setTimeout(() => {{ updateDashboardCharts(); }}, 50);
            }}
        }}

        function applySlicers() {{
            const regVal = document.getElementById('slicer-region').value;
            const statVal = document.getElementById('slicer-status').value;
            const searchVal = document.getElementById('slicer-search').value.toLowerCase().trim();

            filteredRecords = allRecords.filter(r => {{
                const matchReg = !regVal || r['Tên Địa Bàn'] === regVal;
                const matchStat = !statVal || r['Kết Luận Đánh Giá'] === statVal;
                const matchSearch = !searchVal || 
                    String(r['Tên Doanh Nghiệp']).toLowerCase().includes(searchVal) ||
                    String(r['Người Đại Diện']).toLowerCase().includes(searchVal) ||
                    String(r['Mã Hồ Sơ']).toLowerCase().includes(searchVal);
                return matchReg && matchStat && matchSearch;
            }});

            currentPage = 1;
            renderMasterTable();
            updateDashboardCharts();
        }}

        function resetSlicers() {{
            document.getElementById('slicer-region').value = '';
            document.getElementById('slicer-status').value = '';
            document.getElementById('slicer-search').value = '';
            applySlicers();
        }}

        function updateDashboardCharts() {{
            // Budget by Region
            const regMap = {{}};
            filteredRecords.forEach(r => {{
                const reg = r['Mã Địa Bàn'] || 'Khác';
                if (!regMap[reg]) regMap[reg] = 0;
                regMap[reg] += Number(r['Ngân Sách Dự Kiến (VNĐ)']) || 0;
            }});

            const ctx1 = document.getElementById('chart-budget').getContext('2d');
            if (chartBudget) chartBudget.destroy();
            chartBudget = new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: Object.keys(regMap),
                    datasets: [{{
                        label: 'Ngân sách (VNĐ)',
                        data: Object.values(regMap),
                        backgroundColor: ['#2563EB', '#3B82F6', '#94A3B8', '#CBD5E1'],
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: val => (val / 1e9).toFixed(0) + ' Tỷ'
                            }}
                        }}
                    }}
                }}
            }});

            // Gating breakdown
            const gateMap = {{ 'ĐẠT (PASS)': 0, 'FAIL SLA On-site': 0, 'FAIL Lệch WMS': 0 }};
            filteredRecords.forEach(r => {{
                const res = String(r['Kết Luận Đánh Giá'] || '');
                if (res.includes('PASS')) gateMap['ĐẠT (PASS)']++;
                else if (res.includes('SUPPORT')) gateMap['FAIL SLA On-site']++;
                else if (res.includes('PRODUCT')) gateMap['FAIL Lệch WMS']++;
            }});

            const ctx2 = document.getElementById('chart-gating').getContext('2d');
            if (chartGating) chartGating.destroy();
            chartGating = new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(gateMap),
                    datasets: [{{
                        data: Object.values(gateMap),
                        backgroundColor: ['#10B981', '#EF4444', '#F59E0B']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }} }} }}
                    }}
                }}
            }});
        }}

        function getBadge(val) {{
            const s = String(val);
            if (s.includes('PASS') || s.includes('ĐẠT')) return 'badge-pass';
            if (s.includes('SUPPORT') || s.includes('PRODUCT') || s.includes('LOẠI')) return 'badge-fail';
            return 'badge-warn';
        }}

        function renderMasterTable() {{
            const tbody = document.getElementById('master-table-body');
            tbody.innerHTML = '';

            document.getElementById('showing-count').textContent = filteredRecords.length.toLocaleString('vi-VN');

            const start = (currentPage - 1) * pageSize;
            const end = Math.min(start + pageSize, filteredRecords.length);
            const pageData = filteredRecords.slice(start, end);

            pageData.forEach(r => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition-colors';
                tr.innerHTML = `
                    <td class="p-3 font-bold text-slate-900 whitespace-nowrap">${{r['Mã Hồ Sơ']}}</td>
                    <td class="p-3 font-semibold text-slate-600 whitespace-nowrap">${{r['Mã Địa Bàn']}}</td>
                    <td class="p-3 font-medium text-slate-800 whitespace-nowrap">${{r['Tên Doanh Nghiệp']}}</td>
                    <td class="p-3 text-slate-600 whitespace-nowrap">${{r['Mô Hình Bán Lẻ']}}</td>
                    <td class="p-3 text-right font-medium text-slate-700 whitespace-nowrap">${{r['Số Cửa Hàng']}}</td>
                    <td class="p-3 text-right font-bold text-slate-900 whitespace-nowrap">${{Number(r['Ngân Sách Dự Kiến (VNĐ)']).toLocaleString('vi-VN')}} ₫</td>
                    <td class="p-3 text-slate-600 whitespace-nowrap">${{r['Giải Pháp Đang Tìm Hiểu']}}</td>
                    <td class="p-3 whitespace-nowrap">
                        <span class="px-2 py-0.5 rounded text-[11px] font-semibold ${{getBadge(r['Kết Luận Đánh Giá'])}}">
                            ${{r['Kết Luận Đánh Giá'].length > 35 ? r['Kết Luận Đánh Giá'].slice(0, 35) + '...' : r['Kết Luận Đánh Giá']}}
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            }});

            const totalPages = Math.ceil(filteredRecords.length / pageSize) || 1;
            document.getElementById('pagination-info').textContent = `Hiển thị ${{start + 1}}–${{end}} của ${{filteredRecords.length}} (Trang ${{currentPage}}/${{totalPages}})`;
            document.getElementById('btn-prev').disabled = currentPage <= 1;
            document.getElementById('btn-next').disabled = currentPage >= totalPages;
        }}

        function renderSurveyTable() {{
            const tbody = document.getElementById('survey-table-body');
            tbody.innerHTML = '';
            
            // Filter top 10 DB-01 and top 10 DB-02 by Revenue
            const db01 = allRecords.filter(r => r['Mã Địa Bàn'] === 'DB-01').sort((a,b) => b['Doanh Thu Năm (VNĐ)'] - a['Doanh Thu Năm (VNĐ)']).slice(0, 10);
            const db02 = allRecords.filter(r => r['Mã Địa Bàn'] === 'DB-02').sort((a,b) => b['Doanh Thu Năm (VNĐ)'] - a['Doanh Thu Năm (VNĐ)']).slice(0, 10);
            const top20 = [...db01, ...db02];

            top20.forEach(r => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition-colors';
                tr.innerHTML = `
                    <td class="p-3 font-bold text-slate-900 whitespace-nowrap">${{r['Mã Hồ Sơ']}}</td>
                    <td class="p-3 font-bold ${{r['Mã Địa Bàn'] === 'DB-01' ? 'text-emerald-700' : 'text-blue-700'}} whitespace-nowrap">${{r['Mã Địa Bàn']}}</td>
                    <td class="p-3 font-semibold text-slate-800 whitespace-nowrap">${{r['Tên Doanh Nghiệp']}}</td>
                    <td class="p-3 text-slate-600 whitespace-nowrap">${{r['Mô Hình Bán Lẻ']}}</td>
                    <td class="p-3 text-right font-medium text-slate-700 whitespace-nowrap">${{r['Số Cửa Hàng']}}</td>
                    <td class="p-3 text-right font-bold text-slate-900 whitespace-nowrap">${{Number(r['Doanh Thu Năm (VNĐ)']).toLocaleString('vi-VN')}} ₫</td>
                    <td class="p-3 text-indigo-700 font-medium whitespace-nowrap">${{r['Giải Pháp Đang Tìm Hiểu']}}</td>
                    <td class="p-3 text-slate-600 whitespace-nowrap">${{r['Người Đại Diện']}} (${{r['Chức Danh']}})</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function prevPage() {{ if (currentPage > 1) {{ currentPage--; renderMasterTable(); }} }}
        function nextPage() {{ const tp = Math.ceil(filteredRecords.length / pageSize); if (currentPage < tp) {{ currentPage++; renderMasterTable(); }} }}
        function changePageSize() {{ pageSize = Number(document.getElementById('page-size').value); currentPage = 1; renderMasterTable(); }}

        function exportToCSV() {{
            if (!filteredRecords.length) return;
            const headers = Object.keys(filteredRecords[0]);
            const rows = filteredRecords.map(r => headers.map(h => `"${{String(r[h] || '').replace(/"/g, '""')}}"`).join(','));
            const csvContent = "\uFEFF" + [headers.join(','), ...rows].join('\\n');
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "Hung_Phat_WMS_1000_Leads_Cleaned.csv";
            link.click();
        }}
    </script>
</body>
</html>
"""

output_html = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "AI301_Executive_Integrated_Dashboard.html")
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"SUCCESS: Generated integrated executive HTML dashboard at {output_html}")

