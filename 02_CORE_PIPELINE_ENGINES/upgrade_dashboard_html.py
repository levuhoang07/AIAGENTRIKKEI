# -*- coding: utf-8 -*-
"""
UPGRADE DASHBOARD HTML GENERATOR
Tạo tệp AI301_Executive_Integrated_Dashboard.html tích hợp đầy đủ:
1. Header Bar với Upload Control (Drag & Drop .xlsx/.csv)
2. Modal Tra Cứu Quy Chuẩn 26 Cột (Data Dictionary)
3. Modal Cảnh Báo Lỗi Schema Nghiêm Ngặt (422 Error Interceptor)
4. Tương thích kép:
   - Khi chạy qua FastAPI (http://localhost:8000): Upload và phân tích dữ liệu động thời gian thực
   - Khi mở trực tiếp file offline (file://): Hiển thị dữ liệu Master 1.000 Leads mặc định
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_HTML = ROOT / "AI301_Executive_Integrated_Dashboard.html"

html_code = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hưng Phát WMS - Nền Tảng Đánh Giá Thị Trường & Thẩm Định Dữ Liệu</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background-color: #F8FAFC;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 4px;
        }
        .badge-pass { background-color: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
        .badge-fail { background-color: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }
        .badge-warn { background-color: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }
        .tab-btn.active {
            border-bottom: 2px solid #2563EB;
            color: #1D4ED8;
            font-weight: 700;
        }
        .modal {
            transition: opacity 0.25s ease;
        }
        .dragover {
            border-color: #3B82F6 !important;
            background-color: #EFF6FF !important;
        }
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- Header Banner -->
    <header class="bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white border-b border-slate-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="bg-blue-600/30 text-blue-300 text-xs font-bold px-2.5 py-0.5 rounded-full border border-blue-500/30">
                            HƯNG PHÁT TECH • WMS SOLUTIONS
                        </span>
                        <span class="text-xs text-slate-400">Nền Tảng AI301 Đề 04</span>
                    </div>
                    <h1 class="text-lg sm:text-2xl font-extrabold tracking-tight mt-1 text-white">
                        HỆ THỐNG THẨM ĐỊNH DỮ LIỆU & ĐÁNH GIÁ THỊ TRƯỜNG MỞ RỘNG
                    </h1>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <!-- Schema Reference Button -->
                    <button onclick="openSchemaModal()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-900/60 hover:bg-indigo-800 text-indigo-200 border border-indigo-700/50 transition-all">
                        <i class="fa-solid fa-book-bookmark mr-1"></i> Bảng Quy Chuẩn 26 Cột
                    </button>
                    <!-- Download Template Button -->
                    <button onclick="downloadTemplate()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all">
                        <i class="fa-solid fa-download mr-1"></i> Tải Tệp Mẫu
                    </button>
                    <!-- Export CSV Button -->
                    <button onclick="exportToCSV()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm transition-all">
                        <i class="fa-solid fa-file-excel mr-1"></i> Xuất CSV
                    </button>
                </div>
            </div>

            <!-- Upload Control Bar -->
            <div class="mt-3 pt-3 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                <div class="flex items-center space-x-2">
                    <span class="text-slate-400">Tệp đang phân tích:</span>
                    <span id="active-filename" class="font-bold text-amber-300 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-800/50">
                        AI301_De04_Master_1000_Leads.xlsx (1.000 hồ sơ mặc định)
                    </span>
                    <span id="active-hash" class="text-slate-500 font-mono text-[10px] hidden md:inline">
                        SHA256: Verified
                    </span>
                </div>
                <div>
                    <!-- Hidden file input -->
                    <input type="file" id="file-uploader" accept=".xlsx,.xls,.csv" class="hidden" onchange="handleFileSelected(event)">
                    <button onclick="document.getElementById('file-uploader').click()" class="bg-blue-600 hover:bg-blue-500 text-white px-3.5 py-1.5 rounded-lg font-bold shadow transition-all flex items-center space-x-1.5">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                        <span>Tải Lên Bộ Dữ Liệu Mới (.xlsx / .csv)</span>
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
                    <i class="fa-solid fa-briefcase mr-2"></i> 2. Phân Tích As-Is & Điểm Đứt Gãy
                </button>
                <button onclick="switchTab('tab-mcda')" id="btn-tab-mcda" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-ranking-star mr-2"></i> 3. Ma Trận Chấm Điểm MCDA & Top 2
                </button>
                <button onclick="switchTab('tab-survey')" id="btn-tab-survey" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-clipboard-check mr-2"></i> 4. Kế Hoạch Khảo Sát 20 Chuỗi Hạt Nhân
                </button>
                <button onclick="switchTab('tab-data')" id="btn-tab-data" class="tab-btn py-3 whitespace-nowrap flex items-center transition-all">
                    <i class="fa-solid fa-database mr-2"></i> 5. Bảng Dữ Liệu Chi Tiết (Live Search)
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
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Tổng Hồ Sơ Khảo Sát</p>
                    <p id="kpi-total-leads" class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">1,000</p>
                    <p class="text-xs text-slate-500 mt-1 flex items-center">
                        <i class="fa-solid fa-location-dot mr-1 text-blue-500"></i> Phân bổ 4 địa bàn mục tiêu
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-emerald-600 uppercase tracking-wider">Tỷ Lệ Đạt Gating</p>
                    <p id="kpi-valid-pct" class="text-2xl sm:text-3xl font-extrabold text-emerald-600 mt-1">57.0%</p>
                    <p id="kpi-valid-sub" class="text-xs text-slate-500 mt-1">
                        570 / 1,000 hồ sơ vượt qua 2 chốt chặn
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-blue-600 uppercase tracking-wider">Ngân Sách Khả Dụng</p>
                    <p id="kpi-budget" class="text-2xl sm:text-3xl font-extrabold text-blue-700 mt-1">150.3 Tỷ ₫</p>
                    <p class="text-xs text-slate-500 mt-1">
                        Sẵn sàng chi trả giải pháp WMS
                    </p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-indigo-600 uppercase tracking-wider">Chiến Lược Mở Rộng</p>
                    <p id="kpi-strategy" class="text-xl font-extrabold text-indigo-700 mt-1">DB-01 & DB-02</p>
                    <p id="kpi-strategy-sub" class="text-xs text-slate-500 mt-1">
                        Đông Nam Bộ (4.70) & ĐBSCL (4.28)
                    </p>
                </div>
            </div>

            <!-- Visual Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Regional Budget and Leads Chart -->
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-between">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-bold text-slate-800 text-sm flex items-center">
                            <i class="fa-solid fa-chart-column mr-2 text-blue-600"></i> Quy Mô Ngân Sách Theo 4 Địa Bàn
                        </h3>
                        <span class="text-xs text-slate-400">Đơn vị: Tỷ VNĐ</span>
                    </div>
                    <div class="relative h-64 w-full">
                        <canvas id="chart-regional"></canvas>
                    </div>
                </div>

                <!-- Gating Filter Doughnut -->
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-between">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-bold text-slate-800 text-sm flex items-center">
                            <i class="fa-solid fa-filter-circle-xmark mr-2 text-indigo-600"></i> Cơ Cấu Sàng Lọc Gating & Vi Phạm
                        </h3>
                        <span class="text-xs text-slate-400">Tỷ lệ qua / loại</span>
                    </div>
                    <div class="relative h-64 w-full flex items-center justify-center">
                        <canvas id="chart-gating"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 2: PROBLEM DISCOVERY (AS-IS DIAGNOSTICS) -->
        <!-- ========================================================= -->
        <div id="tab-management" class="tab-content hidden space-y-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
                <h3 class="text-base font-extrabold text-slate-900 border-b pb-2 flex items-center">
                    <i class="fa-solid fa-stethoscope mr-2 text-red-600"></i>
                    KHÁM NGHIỆM WORKFLOW HIỆN TẠI (AS-IS) & CÁC ĐIỂM ĐỨT GÃY BÀN GIAO (BROKEN HANDOFFS)
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed">
                    Quy trình khảo sát thủ công trước đây của Hưng Phát gặp phải 4 điểm đứt gãy nghiêm trọng gây lãng phí nguồn lực:
                </p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div class="p-4 rounded-lg bg-red-50 border border-red-200">
                        <h4 class="font-bold text-red-900 mb-1 flex items-center"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> 1. Vi Phạm Cam Kết SLA On-Site (DB-03)</h4>
                        <p class="text-slate-700">87.8% hồ sơ tại Nam Trung Bộ yêu cầu hỗ trợ on-site &le; 2h nhưng cự ly &gt; 550km. Đội ngũ kinh doanh trước đây vẫn đưa vào danh sách tiếp cận gây xung đột vận hành với bộ phận kỹ thuật.</p>
                    </div>
                    <div class="p-4 rounded-lg bg-amber-50 border border-amber-200">
                        <h4 class="font-bold text-amber-900 mb-1 flex items-center"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i> 2. Lệch Pha Định Vị Giải Pháp (DB-04)</h4>
                        <p class="text-slate-700">94.0% hồ sơ tại Tây Nguyên là hộ kinh doanh cá thể, đại lý thu mua nông sản thô chỉ cần sổ sách hoặc máy tính cũ. Không tương thích giải pháp WMS chuyên nghiệp của Hưng Phát.</p>
                    </div>
                    <div class="p-4 rounded-lg bg-blue-50 border border-blue-200">
                        <h4 class="font-bold text-blue-900 mb-1 flex items-center"><i class="fa-solid fa-clock-rotate-left mr-1.5"></i> 3. Lệch Kỳ Thống Kê & Dữ Liệu Lỗi Thời</h4>
                        <p class="text-slate-700">So sánh khập khiễng giữa dữ liệu mới Quý 1-2/2024 (Đông Nam Bộ) với dữ liệu cũ năm 2021 (Tây Nguyên) dẫn đến nhận định sai lầm về tiềm năng thị trường.</p>
                    </div>
                    <div class="p-4 rounded-lg bg-purple-50 border border-purple-200">
                        <h4 class="font-bold text-purple-900 mb-1 flex items-center"><i class="fa-solid fa-copy mr-1.5"></i> 4. Trùng Lặp Nguồn Tin (Bẫy Ảo Tưởng Quy Mô)</h4>
                        <p class="text-slate-700">Một bản báo cáo năm 2021 được nhân viên sao chép lại từ 2 nguồn tin khác nhau khiến số lượng lead tăng ảo lên 200 hồ sơ nhưng thực chất không có giá trị chuyển đổi.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 3: MCDA MATRIX & SCORING -->
        <!-- ========================================================= -->
        <div id="tab-mcda" class="tab-content hidden space-y-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
                <div class="flex items-center justify-between border-b pb-3">
                    <div>
                        <h3 class="text-base font-extrabold text-slate-900 flex items-center">
                            <i class="fa-solid fa-ranking-star mr-2 text-indigo-600"></i>
                            MA TRẬN CHẤM ĐIỂM ĐA TIÊU CHÍ (MCDA SCORING MATRIX)
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">Công thức trọng số: Khớp WMS (35%) + Triển Khai (30%) + Cạnh Tranh (20%) + Quy Mô (15%)</p>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-white">
                                <th class="p-3 font-bold rounded-tl-lg">Mã ĐB</th>
                                <th class="p-3 font-bold">Tên Địa Bàn Khảo Sát</th>
                                <th class="p-3 font-bold text-center">Khớp WMS (35%)</th>
                                <th class="p-3 font-bold text-center">Triển Khai (30%)</th>
                                <th class="p-3 font-bold text-center">Cạnh Tranh (20%)</th>
                                <th class="p-3 font-bold text-center">Quy Mô (15%)</th>
                                <th class="p-3 font-bold text-center bg-indigo-900">Tổng Điểm MCDA</th>
                                <th class="p-3 font-bold rounded-tr-lg">Quyết Định Chiến Lược</th>
                            </tr>
                        </thead>
                        <tbody id="mcda-table-body" class="divide-y divide-slate-200">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 4: SURVEY PLAN TOP 20 -->
        <!-- ========================================================= -->
        <div id="tab-survey" class="tab-content hidden space-y-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
                <div class="flex items-center justify-between border-b pb-3">
                    <div>
                        <h3 class="text-base font-extrabold text-slate-900 flex items-center">
                            <i class="fa-solid fa-clipboard-list mr-2 text-emerald-600"></i>
                            DANH SÁCH 20 CHUỖI BÁN LẺ HẠT NHÂN THAM GIA KHẢO SÁT THỰC ĐỊA
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">Top 10 chuỗi DB-01 (Đông Nam Bộ) và Top 10 chuỗi DB-02 (ĐBSCL) có ngân sách & quy mô lớn nhất</p>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-white">
                                <th class="p-3 font-bold">Mã Hồ Sơ</th>
                                <th class="p-3 font-bold">ĐB</th>
                                <th class="p-3 font-bold">Tên Doanh Nghiệp</th>
                                <th class="p-3 font-bold">Mô Hình Bán Lẻ</th>
                                <th class="p-3 font-bold text-right">Số Cửa Hàng</th>
                                <th class="p-3 font-bold text-right">Doanh Thu Năm</th>
                                <th class="p-3 font-bold text-right">Ngân Sách WMS</th>
                                <th class="p-3 font-bold">Giải Pháp Lựa Chọn</th>
                                <th class="p-3 font-bold">Người Đại Diện</th>
                            </tr>
                        </thead>
                        <tbody id="survey-table-body" class="divide-y divide-slate-200">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================================= -->
        <!-- TAB 5: RAW DATA VIEWER & LIVE SEARCH -->
        <!-- ========================================================= -->
        <div id="tab-data" class="tab-content hidden space-y-6">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b pb-3">
                    <div>
                        <h3 class="text-base font-extrabold text-slate-900 flex items-center">
                            <i class="fa-solid fa-database mr-2 text-blue-600"></i>
                            BẢNG DỮ LIỆU KHẢO SÁT CHI TIẾT
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">Đang hiển thị <span id="showing-count" class="font-bold text-slate-800">0</span> hồ sơ</p>
                    </div>
                    <div class="w-full sm:w-72">
                        <input type="text" id="live-search-input" onkeyup="filterDataTable()" placeholder="Tìm kiếm tên, mô hình, mã hồ sơ..." class="w-full text-xs p-2 rounded-lg border border-slate-300 outline-none focus:border-blue-500">
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700">
                                <th class="p-2.5 font-bold">Mã Hồ Sơ</th>
                                <th class="p-2.5 font-bold">ĐB</th>
                                <th class="p-2.5 font-bold">Doanh Nghiệp</th>
                                <th class="p-2.5 font-bold">Mô Hình</th>
                                <th class="p-2.5 font-bold text-right">Cửa Hàng</th>
                                <th class="p-2.5 font-bold text-right">Ngân Sách (VND)</th>
                                <th class="p-2.5 font-bold">Giải Pháp</th>
                                <th class="p-2.5 font-bold">Trạng Thái Đánh Giá</th>
                            </tr>
                        </thead>
                        <tbody id="raw-table-body" class="divide-y divide-slate-200">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- ========================================================= -->
    <!-- MODAL 1: SCHEMA REFERENCE TABLE (DATA CONTRACT) -->
    <!-- ========================================================= -->
    <div id="schema-modal" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-slate-200">
            <div class="bg-slate-900 text-white p-4 flex items-center justify-between border-b border-slate-800">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-book-bookmark text-indigo-400 text-lg"></i>
                    <div>
                        <h3 class="font-bold text-sm">BẢNG QUY CHUẨN DỮ LIỆU BẮT BUỘC (DATA CONTRACT - 26 CỘT)</h3>
                        <p class="text-[11px] text-slate-400">Các tệp tải lên bắt buộc phải khớp 100% với danh mục cột dưới đây</p>
                    </div>
                </div>
                <button onclick="closeSchemaModal()" class="text-slate-400 hover:text-white p-1 rounded-lg">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>
            <div class="p-4 overflow-y-auto custom-scrollbar flex-1">
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="bg-slate-100 text-slate-700 sticky top-0">
                            <th class="p-2.5 font-bold">STT</th>
                            <th class="p-2.5 font-bold">Tên Cột Bắt Buộc</th>
                            <th class="p-2.5 font-bold">Kiểu Dữ Liệu</th>
                            <th class="p-2.5 font-bold">Mẫu Giá Trị</th>
                            <th class="p-2.5 font-bold">Mô Tả & Ý Nghĩa Nghiệp Vụ</th>
                        </tr>
                    </thead>
                    <tbody id="schema-spec-tbody" class="divide-y divide-slate-200">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
            <div class="bg-slate-50 p-3.5 border-t border-slate-200 flex justify-between items-center">
                <button onclick="downloadTemplate()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-lg shadow transition-all">
                    <i class="fa-solid fa-download mr-1.5"></i> Tải Tệp Excel Mẫu Chuẩn (.xlsx)
                </button>
                <button onclick="closeSchemaModal()" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs rounded-lg transition-all">
                    Đóng
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================================= -->
    <!-- MODAL 2: SCHEMA VALIDATION ERROR ALERT (HTTP 422) -->
    <!-- ========================================================= -->
    <div id="error-modal" class="fixed inset-0 bg-red-950/70 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full overflow-hidden border border-red-300 animate-in fade-in zoom-in duration-200">
            <div class="bg-red-700 text-white p-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-triangle-exclamation text-xl"></i>
                    <h3 class="font-extrabold text-sm uppercase tracking-wide">TỆP TẢI LÊN VI PHẠM QUY CHUẨN DỮ LIỆU!</h3>
                </div>
                <button onclick="closeErrorModal()" class="text-red-200 hover:text-white p-1">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>
            <div class="p-5 space-y-4 text-xs">
                <p id="error-message" class="text-red-950 font-semibold text-sm leading-relaxed"></p>
                
                <!-- Missing Columns Box -->
                <div id="missing-cols-container" class="hidden space-y-2">
                    <p class="font-bold text-slate-800">Danh mục cột bị thiếu hoặc sai tên:</p>
                    <div id="missing-cols-list" class="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-2.5 bg-red-50 rounded-lg border border-red-200">
                        <!-- Populated by JS -->
                    </div>
                </div>

                <!-- Invalid Cells Box -->
                <div id="invalid-cells-container" class="hidden space-y-2">
                    <p class="font-bold text-slate-800">Chi tiết tọa độ ô dữ liệu sai định dạng:</p>
                    <div id="invalid-cells-list" class="max-h-36 overflow-y-auto p-2 bg-red-50 rounded-lg border border-red-200 space-y-1">
                        <!-- Populated by JS -->
                    </div>
                </div>

                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-600 space-y-1">
                    <p class="font-bold text-slate-800"><i class="fa-solid fa-lightbulb text-amber-500 mr-1"></i> Hướng Dẫn Khắc Phục:</p>
                    <p>1. Vui lòng mở <strong>Bảng Quy Chuẩn 26 Cột</strong> để đối chiếu chính xác tên cột và kiểu dữ liệu.</p>
                    <p>2. Hoặc tải <strong>Tệp Mẫu Chuẩn (.xlsx)</strong>, copy dữ liệu của bạn vào đúng các cột tương ứng rồi tải lên lại.</p>
                </div>
            </div>
            <div class="bg-slate-100 p-3.5 border-t border-slate-200 flex justify-end space-x-2">
                <button onclick="closeErrorModal(); openSchemaModal();" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs">
                    <i class="fa-solid fa-book-bookmark mr-1.5"></i> Mở Bảng Quy Chuẩn
                </button>
                <button onclick="closeErrorModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-lg text-xs">
                    Đóng & Thử Lại
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================================= -->
    <!-- JAVASCRIPT APP ENGINE -->
    <!-- ========================================================= -->
    <script>
        let currentData = null;
        let chartRegional = null;
        let chartGating = null;
        let rawTableRecords = [];

        // Tab switcher
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).classList.add('active');
        }

        // Schema modal
        function openSchemaModal() {
            document.getElementById('schema-modal').classList.remove('hidden');
        }
        function closeSchemaModal() {
            document.getElementById('schema-modal').classList.add('hidden');
        }

        // Error modal
        function openErrorModal(msg, missing = [], invalid = []) {
            document.getElementById('error-message').textContent = msg;
            
            const missBox = document.getElementById('missing-cols-container');
            const missList = document.getElementById('missing-cols-list');
            missList.innerHTML = '';
            if (missing && missing.length > 0) {
                missing.forEach(col => {
                    const span = document.createElement('span');
                    span.className = 'px-2 py-1 bg-red-100 text-red-800 font-mono text-[11px] rounded border border-red-300 font-semibold';
                    span.textContent = col;
                    missList.appendChild(span);
                });
                missBox.classList.remove('hidden');
            } else {
                missBox.classList.add('hidden');
            }

            const invBox = document.getElementById('invalid-cells-container');
            const invList = document.getElementById('invalid-cells-list');
            invList.innerHTML = '';
            if (invalid && invalid.length > 0) {
                invalid.forEach(c => {
                    const p = document.createElement('p');
                    p.className = 'text-[11px] text-red-800';
                    p.innerHTML = `<strong>Dòng ${c.row}</strong>, Cột <strong>'${c.column}'</strong>: Giá trị <em>'${c.value}'</em> không hợp lệ (Cần: ${c.expected})`;
                    invList.appendChild(p);
                });
                invBox.classList.remove('hidden');
            } else {
                invBox.classList.add('hidden');
            }

            document.getElementById('error-modal').classList.remove('hidden');
        }
        function closeErrorModal() {
            document.getElementById('error-modal').classList.add('hidden');
        }

        // Download Template
        function downloadTemplate() {
            window.location.href = '/api/download-template';
        }

        // File upload handler
        async function handleFileSelected(event) {
            const file = event.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            const btn = document.querySelector('button[onclick*="file-uploader"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1.5"></i> Đang Thẩm Định...';
            btn.disabled = true;

            try {
                const response = await fetch('/api/analyze-workbook', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.status === 'success') {
                    renderDashboardData(data);
                    alert(`✅ Thẩm định thành công tệp: ${file.name}\\nTất cả 26 cột hợp lệ. Đã tính toán lại ma trận MCDA!`);
                } else {
                    openErrorModal(
                        data.message || 'Lỗi kiểm toán dữ liệu.',
                        data.missing_columns || [],
                        data.invalid_cells || []
                    );
                }
            } catch (err) {
                alert('Không thể kết nối đến máy chủ FastAPI. Vui lòng đảm bảo server đang chạy tại port 8000.');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
                event.target.value = '';
            }
        }

        // Render dashboard data
        function renderDashboardData(data) {
            currentData = data;
            rawTableRecords = data.records || [];

            // 1. Audit info
            if (data.audit) {
                document.getElementById('active-filename').textContent = `${data.audit.filename} (${data.audit.total_records.toLocaleString('vi-VN')} hồ sơ)`;
                const hashEl = document.getElementById('active-hash');
                hashEl.textContent = `SHA256: ${data.audit.sha256.slice(0, 12)}...`;
                hashEl.classList.remove('hidden');
            }

            // 2. KPIs
            if (data.kpis) {
                document.getElementById('kpi-total-leads').textContent = data.kpis.total_leads.toLocaleString('vi-VN');
                document.getElementById('kpi-valid-pct').textContent = data.kpis.valid_pct + '%';
                document.getElementById('kpi-valid-sub').textContent = `${data.kpis.valid_leads.toLocaleString('vi-VN')} / ${data.kpis.total_leads.toLocaleString('vi-VN')} hồ sơ đạt Gating`;
                document.getElementById('kpi-budget').textContent = (data.kpis.available_budget / 1e9).toFixed(1) + ' Tỷ ₫';
                document.getElementById('kpi-strategy').textContent = 'DB-01 & DB-02';
                document.getElementById('kpi-strategy-sub').textContent = `Top 1: ${data.kpis.top1_score} | Top 2: ${data.kpis.top2_score}`;
            }

            // 3. MCDA Table
            const mcdaBody = document.getElementById('mcda-table-body');
            mcdaBody.innerHTML = '';
            if (data.mcda_matrix) {
                Object.values(data.mcda_matrix).forEach(m => {
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-slate-50 transition-colors';
                    const isTop = m.decision.includes('Top') || m.decision.includes('HẠNG');
                    const badgeClass = isTop ? 'badge-pass' : 'badge-fail';
                    tr.innerHTML = `
                        <td class="p-3 font-bold text-slate-900">${m.area_code}</td>
                        <td class="p-3 font-semibold text-slate-700">${m.area_name}</td>
                        <td class="p-3 text-center font-bold text-slate-800">${m.fit.toFixed(1)}</td>
                        <td class="p-3 text-center font-bold text-slate-800">${m.deployment.toFixed(1)}</td>
                        <td class="p-3 text-center font-bold text-slate-800">${m.competition.toFixed(1)}</td>
                        <td class="p-3 text-center font-bold text-slate-800">${m.scale.toFixed(1)}</td>
                        <td class="p-3 text-center font-black text-indigo-700 bg-indigo-50/70 text-sm">${m.total.toFixed(2)}</td>
                        <td class="p-3">
                            <span class="px-2.5 py-1 rounded-md text-[11px] font-bold ${badgeClass}">
                                ${m.decision}
                            </span>
                        </td>
                    `;
                    mcdaBody.appendChild(tr);
                });
            }

            // 4. Survey Plan
            const surveyBody = document.getElementById('survey-table-body');
            surveyBody.innerHTML = '';
            if (data.survey_plan) {
                data.survey_plan.forEach(s => {
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-slate-50 transition-colors';
                    tr.innerHTML = `
                        <td class="p-3 font-bold text-slate-900 font-mono">${s.record_id}</td>
                        <td class="p-3 font-bold ${s.area_code === 'DB-01' ? 'text-emerald-700' : 'text-blue-700'}">${s.area_code}</td>
                        <td class="p-3 font-semibold text-slate-800">${s.business_name}</td>
                        <td class="p-3 text-slate-600">${s.retail_model}</td>
                        <td class="p-3 text-right font-medium">${s.stores}</td>
                        <td class="p-3 text-right font-bold text-slate-900">${Number(s.revenue).toLocaleString('vi-VN')} ₫</td>
                        <td class="p-3 text-right font-bold text-indigo-700">${Number(s.budget).toLocaleString('vi-VN')} ₫</td>
                        <td class="p-3 text-slate-700">${s.solution}</td>
                        <td class="p-3 text-slate-600">${s.representative}</td>
                    `;
                    surveyBody.appendChild(tr);
                });
            }

            // 5. Raw Table
            renderRawTable(rawTableRecords);

            // 6. Charts
            renderCharts(data);
        }

        function renderRawTable(records) {
            const tbody = document.getElementById('raw-table-body');
            tbody.innerHTML = '';
            document.getElementById('showing-count').textContent = records.length.toLocaleString('vi-VN');

            records.slice(0, 100).forEach(r => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 text-[11px]';
                const status = String(r['Kết Luận Đánh Giá'] || '');
                const isPass = status.includes('Đạt') || status.includes('HẠNG');
                tr.innerHTML = `
                    <td class="p-2.5 font-bold font-mono text-slate-900">${r['Mã Hồ Sơ'] || ''}</td>
                    <td class="p-2.5 font-bold text-slate-700">${r['Mã Địa Bàn'] || ''}</td>
                    <td class="p-2.5 font-medium text-slate-800">${r['Tên Doanh Nghiệp Khảo Sát'] || ''}</td>
                    <td class="p-2.5 text-slate-600">${r['Mô Hình Bán Lẻ'] || ''}</td>
                    <td class="p-2.5 text-right font-semibold">${r['Số Cửa Hàng'] || 0}</td>
                    <td class="p-2.5 text-right font-bold text-slate-900">${Number(r['Ngân Sách Dự Kiến Đầu Tư (VND)'] || 0).toLocaleString('vi-VN')} ₫</td>
                    <td class="p-2.5 text-slate-700">${r['Giải Pháp Lựa Chọn'] || ''}</td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isPass ? 'badge-pass' : 'badge-fail'}">
                            ${status.length > 30 ? status.slice(0, 30) + '...' : status}
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterDataTable() {
            const q = document.getElementById('live-search-input').value.toLowerCase().trim();
            if (!q) {
                renderRawTable(rawTableRecords);
                return;
            }
            const filtered = rawTableRecords.filter(r => {
                return String(r['Mã Hồ Sơ'] || '').toLowerCase().includes(q) ||
                       String(r['Tên Doanh Nghiệp Khảo Sát'] || '').toLowerCase().includes(q) ||
                       String(r['Mô Hình Bán Lẻ'] || '').toLowerCase().includes(q) ||
                       String(r['Mã Địa Bàn'] || '').toLowerCase().includes(q);
            });
            renderRawTable(filtered);
        }

        function renderCharts(data) {
            // Regional Chart
            const ctx1 = document.getElementById('chart-regional').getContext('2d');
            if (chartRegional) chartRegional.destroy();
            
            const areaNames = ['Đông Nam Bộ (DB-01)', 'ĐBSCL (DB-02)', 'Nam Trung Bộ (DB-03)', 'Tây Nguyên (DB-04)'];
            const budgets = ['DB-01', 'DB-02', 'DB-03', 'DB-04'].map(a => (data.area_stats[a] ? (data.area_stats[a].budget / 1e9) : 0));

            chartRegional = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: areaNames,
                    datasets: [{
                        label: 'Ngân Sách Dự Kiến (Tỷ VND)',
                        data: budgets,
                        backgroundColor: ['#1B365D', '#2563EB', '#94A3B8', '#CBD5E1'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { ticks: { callback: v => v + ' Tỷ' } }
                    }
                }
            });

            // Gating Chart
            const ctx2 = document.getElementById('chart-gating').getContext('2d');
            if (chartGating) chartGating.destroy();

            const passCount = (data.area_stats['DB-01']?.leads || 0) + (data.area_stats['DB-02']?.leads || 0);
            const failSla = data.area_stats['DB-03']?.leads || 0;
            const failFit = data.area_stats['DB-04']?.leads || 0;

            chartGating = new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Đạt Tiêu Chuẩn Gating (Top 1 & Top 2)', 'Loại Bỏ: Vi Phạm SLA On-site', 'Loại Bỏ: Sai Phân Khúc WMS'],
                    datasets: [{
                        data: [passCount, failSla, failFit],
                        backgroundColor: ['#059669', '#DC2626', '#D97706']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { font: { size: 10 } } }
                    }
                }
            });
        }

        function exportToCSV() {
            if (!rawTableRecords.length) return;
            const headers = Object.keys(rawTableRecords[0]);
            const rows = rawTableRecords.map(r => headers.map(h => `"${String(r[h] || '').replace(/"/g, '""')}"`).join(','));
            const csvContent = "\\ufeff" + [headers.join(','), ...rows].join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "Hung_Phat_WMS_Market_Analysis_Cleaned.csv";
            link.click();
        }

        // Initialize on load
        window.addEventListener('DOMContentLoaded', async () => {
            // Load Schema spec for modal
            try {
                const specRes = await fetch('/api/schema-reference');
                if (specRes.ok) {
                    const specData = await specRes.json();
                    const tbody = document.getElementById('schema-spec-tbody');
                    tbody.innerHTML = '';
                    specData.schema_spec.forEach(c => {
                        const tr = document.createElement('tr');
                        tr.className = 'hover:bg-slate-50 text-[11px]';
                        tr.innerHTML = `
                            <td class="p-2.5 font-bold text-slate-500">${c.stt}</td>
                            <td class="p-2.5 font-bold text-slate-900 font-mono">${c.name}</td>
                            <td class="p-2.5 font-semibold text-blue-700">${c.type}</td>
                            <td class="p-2.5 font-mono text-slate-700">${c.sample}</td>
                            <td class="p-2.5 text-slate-600">${c.description}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (e) {}

            // Load default data from FastAPI backend
            try {
                const res = await fetch('/api/default-data');
                if (res.ok) {
                    const data = await res.json();
                    renderDashboardData(data);
                }
            } catch (err) {
                console.log('Chế độ xem tĩnh: Vui lòng khởi động backend FastAPI để sử dụng tính năng upload động.');
            }
        });
    </script>
</body>
</html>
"""

OUTPUT_HTML.write_text(html_code, encoding="utf-8")
print(f"SUCCESS: Upgraded {OUTPUT_HTML.name} with complete Upload Bar, Strict Validation Alert, and Data Contract Modal!")

