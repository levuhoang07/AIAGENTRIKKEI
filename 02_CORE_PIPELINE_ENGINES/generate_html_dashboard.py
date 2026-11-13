import os
import sys
import json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def build_interactive_html(df, title, subtitle, output_path, kpis=None, category_col=None, value_col=None, status_col=None):
    """
    Builds a standalone, responsive, interactive HTML dashboard using Chart.js, Tailwind CSS, and Vanilla JS.
    Zero local server required. Opens directly in browser.
    """
    # Prepare JSON records for frontend filtering
    records = df.to_dict(orient='records')
    # Clean records for JSON serialization (handle NaN, dates, numpy ints)
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
    columns = list(df.columns)
    
    # Auto detect key columns if not passed
    if not category_col:
        for c in columns:
            if any(k in c.lower() for k in ['địa bàn', 'khu vực', 'nvkd', 'ngành', 'nhóm']):
                category_col = c
                break
        if not category_col:
            category_col = columns[1] if len(columns) > 1 else columns[0]
            
    if not value_col:
        for c in columns:
            if any(k in c.lower() for k in ['ngân sách', 'doanh thu', 'số tiền', 'giá']):
                value_col = c
                break
                
    if not status_col:
        for c in columns:
            if any(k in c.lower() for k in ['trạng thái', 'kết luận', 'thẩm định', 'ưu tiên']):
                status_col = c
                break

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
        .badge-pass {{
            background-color: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
        }}
        .badge-fail {{
            background-color: #FEF2F2;
            color: #B91C1C;
            border: 1px solid #FECACA;
        }}
        .badge-warn {{
            background-color: #FFFBEB;
            color: #B45309;
            border: 1px solid #FDE68A;
        }}
        .badge-default {{
            background-color: #F1F5F9;
            color: #475569;
            border: 1px solid #E2E8F0;
        }}
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen">

    <!-- Top Header Banner -->
    <header class="bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-900 text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <div class="flex items-center space-x-3">
                        <span class="bg-blue-500/20 text-blue-300 text-xs font-bold px-2.5 py-1 rounded-full border border-blue-400/30 uppercase tracking-wider">
                            Executive Dashboard
                        </span>
                        <span class="text-xs text-slate-400 flex items-center">
                            <i class="fa-regular fa-clock mr-1.5"></i> Cập nhật thời gian thực
                        </span>
                    </div>
                    <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight mt-1">{title}</h1>
                    <p class="text-xs sm:text-sm text-slate-300 mt-0.5">{subtitle}</p>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="window.print()" class="inline-flex items-center px-3.5 py-2 text-xs font-semibold rounded-lg bg-white/10 hover:bg-white/20 transition-all text-white border border-white/15">
                        <i class="fa-solid fa-print mr-2"></i> In / Xuất PDF
                    </button>
                    <button onclick="exportToCSV()" class="inline-flex items-center px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 transition-all text-white shadow-sm">
                        <i class="fa-solid fa-file-excel mr-2"></i> Xuất CSV Sạch
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- KPI Metrics Grid -->
        <div id="kpi-container" class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <!-- Dynamic KPI Cards populated by JS -->
        </div>

        <!-- Interactive Slicers Bar -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200/80 p-4">
            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <div class="flex items-center space-x-2 text-slate-700 font-bold text-sm">
                    <i class="fa-solid fa-filter text-indigo-600"></i>
                    <span>Bộ Lọc Đa Chiều (Interactive Slicers):</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1 lg:max-w-3xl">
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Lọc theo {category_col}:</label>
                        <select id="filter-category" onchange="applyFilters()" class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none">
                            <option value="">Tất cả ({category_col})</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Lọc theo {status_col if status_col else 'Trạng Thái'}:</label>
                        <select id="filter-status" onchange="applyFilters()" class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none">
                            <option value="">Tất cả trạng thái</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Tìm kiếm nhanh:</label>
                        <div class="relative">
                            <input type="text" id="filter-search" oninput="applyFilters()" placeholder="Nhập tên đơn vị, mã, người..." class="w-full text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg pl-8 pr-2.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none">
                            <i class="fa-solid fa-magnifying-glass absolute left-2.5 top-2.5 text-slate-400 text-xs"></i>
                        </div>
                    </div>
                </div>
                <div>
                    <button onclick="resetFilters()" class="text-xs text-indigo-600 hover:text-indigo-800 font-semibold underline block text-center lg:text-right">
                        Đặt lại bộ lọc
                    </button>
                </div>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Chart 1 -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200/80 p-5">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-slate-800 flex items-center">
                        <span class="w-2.5 h-2.5 rounded-full bg-blue-600 mr-2"></span>
                        Quy Mô & Phân Bổ Theo {category_col}
                    </h2>
                    <span id="chart1-badge" class="text-xs bg-slate-100 text-slate-600 font-medium px-2 py-0.5 rounded">Toàn bộ</span>
                </div>
                <div class="relative h-64 sm:h-72">
                    <canvas id="chart1"></canvas>
                </div>
            </div>

            <!-- Chart 2 -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200/80 p-5">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-slate-800 flex items-center">
                        <span class="w-2.5 h-2.5 rounded-full bg-indigo-600 mr-2"></span>
                        Cơ Cấu {status_col if status_col else 'Phân Loại'}
                    </h2>
                    <span id="chart2-badge" class="text-xs bg-slate-100 text-slate-600 font-medium px-2 py-0.5 rounded">Tỷ trọng</span>
                </div>
                <div class="relative h-64 sm:h-72">
                    <canvas id="chart2"></canvas>
                </div>
            </div>
        </div>

        <!-- Master Data Table Section -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200/80 overflow-hidden">
            <div class="p-4 sm:p-5 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div>
                    <h2 class="text-base font-bold text-slate-900 flex items-center">
                        <i class="fa-solid fa-table-list text-indigo-600 mr-2"></i>
                        Bảng Dữ Liệu Chi Tiết Đã Làm Sạch
                    </h2>
                    <p class="text-xs text-slate-500 mt-0.5">Hiển thị <span id="showing-count" class="font-bold text-indigo-600">0</span> / <span id="total-count" class="font-bold">0</span> bản ghi</p>
                </div>
                <div class="flex items-center space-x-2 text-xs">
                    <span class="text-slate-500">Hiển thị:</span>
                    <select id="page-size" onchange="changePageSize()" class="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs outline-none">
                        <option value="15">15 dòng</option>
                        <option value="25" selected>25 dòng</option>
                        <option value="50">50 dòng</option>
                        <option value="100">100 dòng</option>
                    </select>
                </div>
            </div>

            <!-- Table Responsive Wrapper -->
            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="bg-slate-100/90 text-slate-700 font-bold uppercase tracking-wider text-[11px] border-b border-slate-200">
                            {''.join([f'<th class="px-4 py-3 whitespace-nowrap">{col}</th>' for col in columns[:8]])}
                        </tr>
                    </thead>
                    <tbody id="table-body" class="divide-y divide-slate-100">
                        <!-- Dynamic Table Rows -->
                    </tbody>
                </table>
            </div>

            <!-- Pagination Bar -->
            <div class="p-4 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-xs text-slate-600">
                <div id="pagination-info">Trang 1 / 1</div>
                <div class="flex items-center space-x-1.5">
                    <button onclick="prevPage()" id="btn-prev" class="px-3 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 font-semibold disabled:opacity-40 disabled:cursor-not-allowed">
                        <i class="fa-solid fa-chevron-left mr-1"></i> Trước
                    </button>
                    <div id="page-numbers" class="flex space-x-1"></div>
                    <button onclick="nextPage()" id="btn-next" class="px-3 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 font-semibold disabled:opacity-40 disabled:cursor-not-allowed">
                        Sau <i class="fa-solid fa-chevron-right ml-1"></i>
                    </button>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-xs text-slate-400">
        Báo cáo tự động sinh từ Hệ thống Chuẩn hóa Dữ liệu BI301 • Hỗ trợ đa nguồn Google Sheets, Lark Base, Excel.
    </footer>

    <!-- Frontend Logic -->
    <script>
        const rawData = {json_data};
        const columns = {json.dumps(columns[:8], ensure_ascii=False)};
        const categoryKey = "{category_col}";
        const valueKey = "{value_col if value_col else ''}";
        const statusKey = "{status_col if status_col else ''}";

        let filteredData = [...rawData];
        let currentPage = 1;
        let pageSize = 25;
        let chart1Instance = null;
        let chart2Instance = null;

        // Init App
        window.addEventListener('DOMContentLoaded', () => {{
            populateFilterOptions();
            applyFilters();
        }});

        function populateFilterOptions() {{
            const catSelect = document.getElementById('filter-category');
            const statusSelect = document.getElementById('filter-status');

            const categories = [...new Set(rawData.map(r => r[categoryKey]).filter(Boolean))].sort();
            categories.forEach(cat => {{
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                catSelect.appendChild(opt);
            }});

            if (statusKey) {{
                const statuses = [...new Set(rawData.map(r => r[statusKey]).filter(Boolean))].sort();
                statuses.forEach(st => {{
                    const opt = document.createElement('option');
                    opt.value = st;
                    opt.textContent = st;
                    statusSelect.appendChild(opt);
                }});
            }}
        }}

        function applyFilters() {{
            const catVal = document.getElementById('filter-category').value;
            const statusVal = document.getElementById('filter-status').value;
            const searchVal = document.getElementById('filter-search').value.toLowerCase().trim();

            filteredData = rawData.filter(row => {{
                const matchCat = !catVal || row[categoryKey] === catVal;
                const matchStatus = !statusVal || (statusKey && row[statusKey] === statusVal);
                const matchSearch = !searchVal || Object.values(row).some(v => String(v).toLowerCase().includes(searchVal));
                return matchCat && matchStatus && matchSearch;
            }});

            currentPage = 1;
            updateKPIs();
            updateCharts();
            renderTable();
        }}

        function resetFilters() {{
            document.getElementById('filter-category').value = '';
            document.getElementById('filter-status').value = '';
            document.getElementById('filter-search').value = '';
            applyFilters();
        }}

        function formatCurrencyVND(val) {{
            const num = Number(val);
            if (isNaN(num)) return val;
            if (num >= 1e12) return (num / 1e12).toFixed(2) + ' Nghìn Tỷ ₫';
            if (num >= 1e9) return (num / 1e9).toFixed(2) + ' Tỷ ₫';
            if (num >= 1e6) return (num / 1e6).toFixed(1) + ' Tr ₫';
            return num.toLocaleString('vi-VN') + ' ₫';
        }}

        function updateKPIs() {{
            const total = filteredData.length;
            let sumVal = 0;
            if (valueKey) {{
                sumVal = filteredData.reduce((acc, r) => acc + (Number(r[valueKey]) || 0), 0);
            }}

            let passCount = 0;
            if (statusKey) {{
                passCount = filteredData.filter(r => {{
                    const s = String(r[statusKey]).toLowerCase();
                    return s.includes('pass') || s.includes('đạt') || s.includes('đã phân công') || s.includes('ưu tiên 1');
                }}).length;
            }}

            const passRate = total > 0 ? ((passCount / total) * 100).toFixed(1) + '%' : '0%';

            const kpiContainer = document.getElementById('kpi-container');
            kpiContainer.innerHTML = `
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Tổng Số Bản Ghi</p>
                    <p class="text-2xl font-extrabold text-slate-900 mt-1">${{total.toLocaleString('vi-VN')}}</p>
                    <p class="text-[11px] text-slate-400 mt-1">Hồ sơ sau lọc</p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                    <p class="text-xs font-semibold text-emerald-600 uppercase">Tỷ Lệ Đạt Chuẩn</p>
                    <p class="text-2xl font-extrabold text-emerald-600 mt-1">${{passRate}}</p>
                    <p class="text-[11px] text-slate-400 mt-1">${{passCount.toLocaleString('vi-VN')}} hồ sơ hợp lệ</p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                    <p class="text-xs font-semibold text-blue-600 uppercase">Tổng Quy Mô Ngân Sách</p>
                    <p class="text-2xl font-extrabold text-blue-700 mt-1">${{formatCurrencyVND(sumVal)}}</p>
                    <p class="text-[11px] text-slate-400 mt-1">${{total > 0 ? formatCurrencyVND(sumVal / total) + ' / đơn vị' : '0 ₫'}}</p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80">
                    <p class="text-xs font-semibold text-indigo-600 uppercase">Độ Bao Phủ Nhóm</p>
                    <p class="text-2xl font-extrabold text-indigo-700 mt-1">${{new Set(filteredData.map(r => r[categoryKey])).size}}</p>
                    <p class="text-[11px] text-slate-400 mt-1">Phân khúc / Nhóm hoạt động</p>
                </div>
            `;
        }}

        function updateCharts() {{
            // Chart 1: Category counts / values
            const catMap = {{}};
            filteredData.forEach(r => {{
                const cat = r[categoryKey] || 'Khác';
                if (!catMap[cat]) catMap[cat] = {{ count: 0, val: 0 }};
                catMap[cat].count++;
                if (valueKey) catMap[cat].val += (Number(r[valueKey]) || 0);
            }});

            const sortedCats = Object.keys(catMap).sort((a,b) => catMap[b].count - catMap[a].count).slice(0, 10);
            const labels1 = sortedCats.map(c => c.length > 20 ? c.slice(0, 20) + '...' : c);
            const data1 = sortedCats.map(c => catMap[c].count);

            const ctx1 = document.getElementById('chart1').getContext('2d');
            if (chart1Instance) chart1Instance.destroy();
            chart1Instance = new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: labels1,
                    datasets: [{{
                        label: 'Số lượng hồ sơ',
                        data: data1,
                        backgroundColor: '#3B82F6',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: '#F1F5F9' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // Chart 2: Status Breakdown
            const statusMap = {{}};
            filteredData.forEach(r => {{
                const st = (statusKey && r[statusKey]) ? r[statusKey] : 'Chưa phân loại';
                statusMap[st] = (statusMap[st] || 0) + 1;
            }});

            const labels2 = Object.keys(statusMap);
            const data2 = Object.values(statusMap);
            const bgColors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6', '#64748B'];

            const ctx2 = document.getElementById('chart2').getContext('2d');
            if (chart2Instance) chart2Instance.destroy();
            chart2Instance = new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: labels2,
                    datasets: [{{
                        data: data2,
                        backgroundColor: bgColors.slice(0, labels2.length)
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }}

        function getBadgeClass(val) {{
            const str = String(val).toLowerCase();
            if (str.includes('pass') || str.includes('đạt') || str.includes('đã phân công') || str.includes('cao')) return 'badge-pass';
            if (str.includes('fail') || str.includes('loại') || str.includes('từ chối') || str.includes('thấp')) return 'badge-fail';
            if (str.includes('chờ') || str.includes('duyệt') || str.includes('trung bình') || str.includes('cảnh báo')) return 'badge-warn';
            return 'badge-default';
        }}

        function renderTable() {{
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';

            document.getElementById('total-count').textContent = rawData.length.toLocaleString('vi-VN');
            document.getElementById('showing-count').textContent = filteredData.length.toLocaleString('vi-VN');

            const startIdx = (currentPage - 1) * pageSize;
            const endIdx = Math.min(startIdx + pageSize, filteredData.length);
            const pageRecords = filteredData.slice(startIdx, endIdx);

            if (pageRecords.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="${{columns.length}}" class="text-center py-8 text-slate-400">Không tìm thấy bản ghi nào phù hợp.</td></tr>`;
                document.getElementById('pagination-info').textContent = 'Trang 0 / 0';
                document.getElementById('btn-prev').disabled = true;
                document.getElementById('btn-next').disabled = true;
                return;
            }}

            pageRecords.forEach(row => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/80 transition-colors';
                
                columns.forEach((col, idx) => {{
                    const td = document.createElement('td');
                    td.className = 'px-4 py-2.5 whitespace-nowrap text-slate-700';
                    const val = row[col];

                    if (idx === 0) {{
                        td.className += ' font-bold text-slate-900';
                        td.textContent = val;
                    }} else if (col === statusKey || col.toLowerCase().includes('trạng thái') || col.toLowerCase().includes('kết luận') || col.toLowerCase().includes('ưu tiên')) {{
                        td.innerHTML = `<span class="px-2 py-0.5 rounded text-[11px] font-semibold ${{getBadgeClass(val)}}">${{val}}</span>`;
                    }} else if (col === valueKey || col.toLowerCase().includes('ngân sách') || col.toLowerCase().includes('doanh thu')) {{
                        td.className += ' text-right font-medium text-slate-900';
                        td.textContent = Number(val).toLocaleString('vi-VN') + ' ₫';
                    }} else {{
                        td.textContent = val;
                    }}
                    tr.appendChild(td);
                }});
                tbody.appendChild(tr);
            }});

            const totalPages = Math.ceil(filteredData.length / pageSize) || 1;
            document.getElementById('pagination-info').textContent = `Hiển thị ${{startIdx + 1}}–${{endIdx}} của ${{filteredData.length.toLocaleString('vi-VN')}} (Trang ${{currentPage}}/${{totalPages}})`;

            document.getElementById('btn-prev').disabled = currentPage <= 1;
            document.getElementById('btn-next').disabled = currentPage >= totalPages;
        }}

        function prevPage() {{
            if (currentPage > 1) {{
                currentPage--;
                renderTable();
            }}
        }}

        function nextPage() {{
            const totalPages = Math.ceil(filteredData.length / pageSize);
            if (currentPage < totalPages) {{
                currentPage++;
                renderTable();
            }}
        }}

        function changePageSize() {{
            pageSize = Number(document.getElementById('page-size').value);
            currentPage = 1;
            renderTable();
        }}

        function exportToCSV() {{
            if (!filteredData.length) return;
            const headers = Object.keys(filteredData[0]);
            const rows = filteredData.map(r => headers.map(h => `"${{String(r[h] || '').replace(/"/g, '""')}}"`).join(','));
            const csvContent = "\uFEFF" + [headers.join(','), ...rows].join('\\n');
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "{os.path.splitext(os.path.basename(output_path))[0]}_Export.csv";
            link.click();
        }}
    </script>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"SUCCESS: Generated interactive HTML dashboard at {output_path}")

if __name__ == '__main__':
    # Test on Nam Viet Leads
    df_nv = pd.read_excel('Nam_Viet_100_Leads_Cleaned.xlsx', sheet_name='Dữ liệu nguồn ')
    build_interactive_html(
        df=df_nv,
        title="DASHBOARD ĐIỀU PHỐI KHÁCH HÀNG TIỀM NĂNG - CÔNG TY NAM VIỆT",
        subtitle="Hệ thống báo cáo CRM trực quan tích hợp bộ lọc đa chiều (Slicers) & Phân bổ 8 NVKD",
        output_path="c:\\antigraviti\\Nam_Viet_100_Leads_Dashboard.html",
        category_col="Nhóm Ngành Chuẩn Hóa",
        value_col="Ngân Sách (VNĐ)",
        status_col="Trạng Thái Xử Lý"
    )

    # Test on AI301 1000 Leads
    df_ai = pd.read_excel('AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx', sheet_name='Dữ liệu nguồn ')
    build_interactive_html(
        df=df_ai,
        title="BÁO CÁO THẨM ĐỊNH & LỰA CHỌN ĐỊA BÀN MỞ RỘNG (HƯNG PHÁT WMS)",
        subtitle="Khảo sát 1.000 chuỗi bán lẻ trên 4 địa bàn, sàng lọc Gating Filter & chấm điểm MCDA",
        output_path="c:\\antigraviti\\AI301_1000_Leads_Dashboard.html",
        category_col="Tên Địa Bàn",
        value_col="Ngân Sách Dự Kiến (VNĐ)",
        status_col="Kết Luận Đánh Giá"
    )

