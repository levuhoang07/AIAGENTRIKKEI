# -*- coding: utf-8 -*-
"""
Production UI v4.1 Updater:
- Espresso Sidebar: hover animation (opens on hover, closes normally), click pin toggle, zero demo buttons
- Kanban cards: smooth hover motion (translateY + shadow + scale) and soft rounded corners (rounded-2xl / 24px)
- Tables: soft rounded container (1.5rem) with zero sharp corners
- Background: fluted wood timber with Latte frosted glass canvas (translucent + blur)
- Typography: Plus Jakarta Sans + Outfit with anti-aliasing
- Empty state: clean minimalist dropzone with central terracotta sparkle, zero verbose text
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "public" / "index.html"
ROOT_HTML = BASE_DIR / "AI301_Executive_Integrated_Dashboard.html"

# Load existing index.html
content = INDEX_HTML.read_text(encoding="utf-8")

# 1. Update CSS in <style>
enhanced_css = """
        :root {
            --glass-canvas-bg: rgba(246, 239, 233, 0.86);
            --glass-canvas-border: rgba(255, 255, 255, 0.75);
            --espresso-sidebar: rgba(46, 31, 24, 0.90);
            --latte-card-bg: rgba(255, 255, 255, 0.85);
            --latte-card-border: rgba(255, 255, 255, 0.95);
        }

        body {
            /* Warm fluted wood paneling aesthetic from reference image */
            background: 
                repeating-linear-gradient(
                    90deg,
                    #22140f 0px,
                    #2c1a14 14px,
                    #382119 28px,
                    #261712 42px,
                    #1d110d 56px
                );
            background-color: #22140f;
            background-attachment: fixed;
            color: #281B17;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }

        /* Giant Main Frosted Glass Canvas */
        .glass-canvas {
            background: var(--glass-canvas-bg);
            backdrop-filter: blur(36px) saturate(170%);
            -webkit-backdrop-filter: blur(36px) saturate(170%);
            border: 1px solid var(--glass-canvas-border);
            box-shadow: 0 35px 80px -15px rgba(0, 0, 0, 0.55), inset 0 1px 2px rgba(255, 255, 255, 0.9);
            border-radius: 2.25rem;
        }

        /* Espresso Floating Sidebar - Auto Hover Animation */
        .espresso-sidebar {
            background: var(--espresso-sidebar);
            backdrop-filter: blur(32px) saturate(180%);
            -webkit-backdrop-filter: blur(32px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.14);
            box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);
            border-radius: 2rem;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Desktop Hover-to-Expand Animation */
        @media (min-width: 1024px) {
            .espresso-sidebar {
                width: 78px;
                overflow: hidden;
            }
            .espresso-sidebar:hover,
            .espresso-sidebar.is-pinned {
                width: 268px;
                box-shadow: 0 30px 80px -10px rgba(0, 0, 0, 0.65), inset 0 1px 1px rgba(255, 255, 255, 0.3);
            }
            
            /* Text elements that smoothly collapse and expand on hover */
            .sidebar-expandable {
                opacity: 0;
                max-width: 0;
                display: inline-block;
                overflow: hidden;
                white-space: nowrap;
                vertical-align: middle;
                transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), max-width 0.35s cubic-bezier(0.16, 1, 0.3, 1);
                pointer-events: none;
            }
            .espresso-sidebar:hover .sidebar-expandable,
            .espresso-sidebar.is-pinned .sidebar-expandable {
                opacity: 1;
                max-width: 190px;
                pointer-events: auto;
            }

            .sidebar-toggle-icon {
                transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .espresso-sidebar:hover .sidebar-toggle-icon,
            .espresso-sidebar.is-pinned .sidebar-toggle-icon {
                transform: rotate(180deg);
            }
        }

        /* Active Sidebar Navigation Pill */
        .nav-pill-active {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.22) 0%, rgba(255, 255, 255, 0.10) 100%);
            border: 1px solid rgba(255, 255, 255, 0.35);
            box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.4), 0 4px 15px rgba(0, 0, 0, 0.25);
            color: #FFFFFF !important;
            font-weight: 700;
        }

        /* Warm Frosted Glass Kanban Cards with Motion on Hover */
        .glass-card {
            background: var(--latte-card-bg);
            backdrop-filter: blur(24px) saturate(160%);
            -webkit-backdrop-filter: blur(24px) saturate(160%);
            border: 1px solid var(--latte-card-border);
            box-shadow: 0 4px 20px -2px rgba(46, 31, 24, 0.05), inset 0 1px 1px rgba(255, 255, 255, 0.95);
            border-radius: 1.5rem; /* Bo tròn 24px mềm mại */
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.28s ease, background-color 0.28s ease;
        }
        .glass-card:hover {
            transform: translateY(-5px) scale(1.008); /* Chuyển động nổi lên rõ rệt khi di chuột */
            box-shadow: 0 20px 40px -8px rgba(46, 31, 24, 0.16), 0 0 0 1px rgba(234, 88, 12, 0.25);
            border-color: rgba(234, 88, 12, 0.35);
            background: rgba(255, 255, 255, 0.95);
        }

        /* Rounded Table Wrapper with Zero Sharp Corners */
        .table-rounded-box {
            border-radius: 1.5rem; /* 24px bo tròn hoàn toàn */
            overflow: hidden;
            border: 1px solid rgba(220, 205, 195, 0.8);
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 4px 15px -2px rgba(46, 31, 24, 0.04);
        }
        .table-rounded-box table {
            border-collapse: separate;
            border-spacing: 0;
        }
        .table-rounded-box table thead tr th:first-child {
            border-top-left-radius: 1.5rem;
        }
        .table-rounded-box table thead tr th:last-child {
            border-top-right-radius: 1.5rem;
        }
        .table-rounded-box table tbody tr:last-child td:first-child {
            border-bottom-left-radius: 1.5rem;
        }
        .table-rounded-box table tbody tr:last-child td:last-child {
            border-bottom-right-radius: 1.5rem;
        }
        .table-rounded-box table tbody tr {
            transition: background-color 0.2s ease;
        }
        .table-rounded-box table tbody tr:hover {
            background-color: rgba(251, 146, 60, 0.08);
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 9999px;
        }

        .drag-overlay {
            display: none;
        }
        body.dragging .drag-overlay {
            display: flex;
        }
"""

# Replace <style>...</style> block
style_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL)
content = style_pattern.sub(f"<style>{enhanced_css}    </style>", content)

# 2. Update Sidebar HTML to have sidebar-expandable spans
new_sidebar = """        <!-- ========================================================= -->
        <!-- 1. ESPRESSO GLASS FLOATING SIDEBAR (HOVER ANIMATION + PIN) -->
        <!-- ========================================================= -->
        <aside id="main-sidebar" class="espresso-sidebar w-full lg:w-[78px] p-4 lg:p-3.5 flex flex-col justify-between shrink-0 lg:sticky lg:top-6 lg:h-[calc(100vh-3rem)] z-40 text-stone-300">
            <div class="space-y-5">
                <!-- Top Brand Header with Terracotta Circular Badge -->
                <div class="flex items-center justify-between pb-2 border-b border-white/10">
                    <div class="flex items-center space-x-3 min-w-0">
                        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-orange-600 via-amber-600 to-red-600 flex items-center justify-center text-white font-black text-sm shadow-lg shadow-orange-950/40 shrink-0">
                            HP
                        </div>
                        <div class="sidebar-expandable">
                            <h1 class="font-extrabold text-sm tracking-tight text-white leading-tight">Hưng Phát WMS</h1>
                            <span class="text-[10px] font-semibold text-stone-400 uppercase tracking-wider block">AI Market Agent</span>
                        </div>
                    </div>
                    <!-- Round Collapse / Pin Toggle Button -->
                    <button onclick="toggleSidebarPin()" title="Ghim hoặc mở rộng thanh công cụ" class="w-7 h-7 rounded-full bg-white/10 hover:bg-white/20 text-stone-300 hover:text-white flex items-center justify-center text-xs transition-all cursor-pointer shrink-0">
                        <i class="fa-solid fa-chevron-left sidebar-toggle-icon text-[10px]"></i>
                    </button>
                </div>

                <!-- Green Active Status Capsule (Matches Reference Image) -->
                <div class="px-2.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 flex items-center justify-between text-xs overflow-hidden">
                    <div class="flex items-center space-x-2 shrink-0">
                        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>
                        <span class="sidebar-expandable text-[11px] font-bold text-emerald-200">AI Workflow Engine</span>
                    </div>
                    <span class="sidebar-expandable text-[9px] font-black uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full ml-auto">ACTIVE</span>
                </div>

                <!-- Navigation Section -->
                <div>
                    <p class="sidebar-expandable text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-2 px-2">ĐIỀU HƯỚNG</p>
                    <nav class="space-y-1.5">
                        <button onclick="switchTab('tab-dashboard')" id="nav-tab-dashboard" title="Tổng Quan Đánh Giá" class="nav-item nav-pill-active w-full flex items-center justify-between p-2.5 rounded-2xl text-xs font-semibold text-stone-300 hover:text-white transition-all cursor-pointer">
                            <div class="flex items-center space-x-3 min-w-0">
                                <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-chart-line text-sm text-stone-300"></i>
                                </div>
                                <span class="sidebar-expandable font-bold truncate">Tổng Quan Đánh Giá</span>
                            </div>
                            <span class="sidebar-expandable text-[10px] bg-white/20 px-2 py-0.5 rounded-full font-bold ml-auto shrink-0">4 ĐB</span>
                        </button>

                        <button onclick="switchTab('tab-management')" id="nav-tab-management" title="Sàng Lọc Gating & SLA" class="nav-item w-full flex items-center justify-between p-2.5 rounded-2xl text-xs font-semibold text-stone-300 hover:text-white hover:bg-white/5 transition-all cursor-pointer">
                            <div class="flex items-center space-x-3 min-w-0">
                                <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-shield-halved text-sm text-stone-400"></i>
                                </div>
                                <span class="sidebar-expandable font-bold truncate">Sàng Lọc Gating & SLA</span>
                            </div>
                            <span class="sidebar-expandable text-[10px] bg-white/10 px-2 py-0.5 rounded-full text-stone-400 font-bold ml-auto shrink-0">3 Rules</span>
                        </button>

                        <button onclick="switchTab('tab-mcda')" id="nav-tab-mcda" title="Ma Trận MCDA (Top 2)" class="nav-item w-full flex items-center justify-between p-2.5 rounded-2xl text-xs font-semibold text-stone-300 hover:text-white hover:bg-white/5 transition-all cursor-pointer">
                            <div class="flex items-center space-x-3 min-w-0">
                                <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-ranking-star text-sm text-stone-400"></i>
                                </div>
                                <span class="sidebar-expandable font-bold truncate">Ma Trận MCDA (Top 2)</span>
                            </div>
                            <span class="sidebar-expandable text-[10px] bg-white/10 px-2 py-0.5 rounded-full text-stone-400 font-bold ml-auto shrink-0">Top 2</span>
                        </button>

                        <button onclick="switchTab('tab-survey')" id="nav-tab-survey" title="Kế Hoạch Khảo Sát" class="nav-item w-full flex items-center justify-between p-2.5 rounded-2xl text-xs font-semibold text-stone-300 hover:text-white hover:bg-white/5 transition-all cursor-pointer">
                            <div class="flex items-center space-x-3 min-w-0">
                                <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-clipboard-check text-sm text-stone-400"></i>
                                </div>
                                <span class="sidebar-expandable font-bold truncate">Kế Hoạch Khảo Sát</span>
                            </div>
                            <span class="sidebar-expandable text-[10px] bg-white/10 px-2 py-0.5 rounded-full text-stone-400 font-bold ml-auto shrink-0">20 Chuỗi</span>
                        </button>

                        <button onclick="switchTab('tab-data')" id="nav-tab-data" title="Dữ Liệu Khảo Sát" class="nav-item w-full flex items-center justify-between p-2.5 rounded-2xl text-xs font-semibold text-stone-300 hover:text-white hover:bg-white/5 transition-all cursor-pointer">
                            <div class="flex items-center space-x-3 min-w-0">
                                <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                    <i class="fa-solid fa-database text-sm text-stone-400"></i>
                                </div>
                                <span class="sidebar-expandable font-bold truncate">Dữ Liệu Khảo Sát</span>
                            </div>
                            <span class="sidebar-expandable text-[10px] bg-white/10 px-2 py-0.5 rounded-full text-stone-400 font-bold ml-auto shrink-0">Raw</span>
                        </button>
                    </nav>
                </div>

                <!-- Action Tools Section (No demo buttons, only standards & blank template) -->
                <div class="pt-2 border-t border-white/10">
                    <p class="sidebar-expandable text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-2 px-2">QUY CHUẨN DỮ LIỆU</p>
                    <div class="space-y-1.5">
                        <button onclick="openSchemaModal()" title="Bảng Quy Chuẩn 26 Cột" class="w-full flex items-center space-x-3 p-2.5 rounded-2xl text-xs font-semibold text-stone-200 bg-white/5 hover:bg-white/10 transition-all border border-white/10 cursor-pointer">
                            <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                <i class="fa-solid fa-book-bookmark text-amber-400 text-sm"></i>
                            </div>
                            <span class="sidebar-expandable truncate">Bảng Quy Chuẩn 26 Cột</span>
                        </button>
                        <button onclick="downloadTemplate()" title="Tải Cấu Trúc File Mẫu" class="w-full flex items-center space-x-3 p-2.5 rounded-2xl text-xs font-semibold text-stone-200 bg-white/5 hover:bg-white/10 transition-all border border-white/10 cursor-pointer">
                            <div class="w-6 h-6 rounded-lg flex items-center justify-center shrink-0">
                                <i class="fa-solid fa-file-arrow-down text-emerald-400 text-sm"></i>
                            </div>
                            <span class="sidebar-expandable truncate">Tải Cấu Trúc File Mẫu</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Sidebar Bottom Footer: Dynamic State Indicator -->
            <div class="mt-6 p-2.5 rounded-2xl bg-white/5 border border-white/10 text-xs">
                <div class="flex items-center space-x-2 text-stone-400">
                    <i id="sidebar-status-dot" class="fa-solid fa-circle-pause text-amber-400 text-[10px] shrink-0"></i>
                    <span id="sidebar-status-text" class="sidebar-expandable text-[10px] font-bold uppercase tracking-wider text-stone-300">Chờ Dữ Liệu</span>
                </div>
                <p id="active-filename" class="sidebar-expandable font-bold text-stone-200 truncate text-[11px] mt-1">Chưa nạp tệp</p>
            </div>
        </aside>"""

# Find and replace sidebar
aside_pattern = re.compile(r'<!-- 1\. ESPRESSO GLASS FLOATING SIDEBAR.*?<\/aside>', re.DOTALL)
content = aside_pattern.sub(new_sidebar, content)

# 3. Add toggleSidebarPin JS function
pin_js = """
        // Sidebar Pin / Unpin Toggle
        function toggleSidebarPin() {
            const sidebar = document.getElementById('main-sidebar');
            if (sidebar) {
                sidebar.classList.toggle('is-pinned');
            }
        }
"""
if "toggleSidebarPin" not in content:
    content = content.replace("function switchTab(", pin_js + "\n        function switchTab(")

# Write updated content
INDEX_HTML.write_text(content, encoding="utf-8")
ROOT_HTML.write_text(content, encoding="utf-8")
print("SUCCESS: Both public/index.html and AI301_Executive_Integrated_Dashboard.html upgraded to v4.1!")
