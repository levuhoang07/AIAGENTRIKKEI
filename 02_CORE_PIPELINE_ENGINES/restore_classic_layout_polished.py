# -*- coding: utf-8 -*-
"""
Restore Classic Dashboard Layout while applying the requested visual polish:
- 100% Classic Layout (4 Main Kanban Cards, Original Tabs, Original Header)
- Translucent Glassmorphism background with soft ambient gradients
- Smooth Kanban Cards hover motion (translateY(-5px) scale(1.008) + glow + shadow)
- Soft rounded corners on all cards and tables (rounded-2xl / 24px)
- Sidebar with auto hover open/close animation (76px -> 272px), zero test demo buttons
- Google Fonts: Plus Jakarta Sans for pristine typography
- Minimalist elegant dropzone without verbose text
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "public" / "index.html"
ROOT_HTML = BASE_DIR / "AI301_Executive_Integrated_Dashboard.html"
V3_SCRIPT = BASE_DIR / "02_CORE_PIPELINE_ENGINES" / "apply_ui_polish_v3.py"

# Read HTML_V3 from apply_ui_polish_v3.py
with open(V3_SCRIPT, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = 'HTML_V3 = """'
end_marker = '"""\n\nINDEX_HTML.write_text'
start_idx = text.find(start_marker) + len(start_marker)
end_idx = text.find(end_marker, start_idx)
html = text[start_idx:end_idx]

# 1. Update Typography to Plus Jakarta Sans
old_font = re.compile(r'<link.*fonts\.googleapis\.com/css2\?family=Be\+Vietnam\+Pro.*?>', re.DOTALL)
new_font = '<link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">'
html = old_font.sub(new_font, html)

# In tailwind config:
html = html.replace(
    "sans: ['\"Inter\"', '\"Be Vietnam Pro\"', 'system-ui', 'sans-serif'],",
    "sans: ['\"Plus Jakarta Sans\"', 'system-ui', '-apple-system', 'sans-serif'],"
)

# 2. Refine Background and Glassmorphism CSS in <style>
old_style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if old_style_match:
    enhanced_css = """
        :root {
            --glass-bg: rgba(255, 255, 255, 0.78);
            --glass-bg-hover: rgba(255, 255, 255, 0.94);
            --glass-border: rgba(255, 255, 255, 0.85);
            --glass-border-hover: rgba(59, 130, 246, 0.45);
            --glass-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05), inset 0 1px 2px rgba(255, 255, 255, 0.95);
            --glass-shadow-hover: 0 20px 40px -10px rgba(37, 99, 235, 0.16), 0 0 0 1px rgba(59, 130, 246, 0.35);
        }

        body {
            /* Nền trong suốt mờ ảo đa tầng với gradient mềm mại tạo chiều sâu chân thực */
            background: 
                radial-gradient(circle at 10% 15%, rgba(219, 234, 254, 0.8) 0%, transparent 45%),
                radial-gradient(circle at 90% 10%, rgba(224, 231, 255, 0.7) 0%, transparent 45%),
                radial-gradient(circle at 50% 85%, rgba(243, 232, 255, 0.6) 0%, transparent 50%),
                radial-gradient(circle at 80% 85%, rgba(219, 234, 254, 0.65) 0%, transparent 45%),
                linear-gradient(135deg, #F8FAFC 0%, #EEF2F6 100%);
            background-attachment: fixed;
            color: #0F172A;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Glassmorphic Kanban Cards with Realistic Lift & Glow Animation */
        .kanban-card {
            background: var(--glass-bg);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
            border-radius: 1.5rem; /* Bo tròn 24px mềm mại */
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, background 0.3s ease;
        }
        .kanban-card:hover {
            transform: translateY(-5px) scale(1.008); /* Chuyển động nổi lên rõ rệt khi rê chuột */
            box-shadow: var(--glass-shadow-hover);
            border-color: var(--glass-border-hover);
            background: var(--glass-bg-hover);
        }

        /* Collapsible Smooth Animated Sidebar (Mở ra khi di chuột, đóng lại bình thường) */
        aside.sidebar-collapsible {
            width: 4.75rem; /* ~76px */
            transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease;
            will-change: width;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border-right: 1px solid rgba(226, 232, 240, 0.85);
        }
        aside.sidebar-collapsible:hover,
        aside.sidebar-collapsible.is-pinned {
            width: 17rem; /* ~272px */
            box-shadow: 12px 0 40px -5px rgba(15, 23, 42, 0.10);
        }
        .sidebar-text {
            opacity: 0;
            transform: translateX(-10px);
            transition: opacity 0.22s ease, transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
            white-space: nowrap;
            pointer-events: none;
            display: inline-block;
        }
        aside.sidebar-collapsible:hover .sidebar-text,
        aside.sidebar-collapsible.is-pinned .sidebar-text {
            opacity: 1;
            transform: translateX(0);
            pointer-events: auto;
            transition-delay: 0.06s;
        }

        /* Soft Rounded Tables with Zero Sharp Edges */
        .table-rounded-container {
            border-radius: 1.5rem; /* Bo tròn 24px hoàn toàn */
            overflow: hidden;
            border: 1px solid rgba(226, 232, 240, 0.9);
            box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04);
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(20px);
        }
        .table-rounded-container table {
            border-collapse: separate;
            border-spacing: 0;
        }
        .table-rounded-container table thead tr th:first-child {
            border-top-left-radius: 1.5rem;
        }
        .table-rounded-container table thead tr th:last-child {
            border-top-right-radius: 1.5rem;
        }
        .table-rounded-container table tbody tr:last-child td:first-child {
            border-bottom-left-radius: 1.5rem;
        }
        .table-rounded-container table tbody tr:last-child td:last-child {
            border-bottom-right-radius: 1.5rem;
        }
        .table-rounded-container table tbody tr {
            transition: background-color 0.18s ease;
        }
        .table-rounded-container table tbody tr:hover {
            background-color: rgba(239, 246, 255, 0.75);
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 9999px;
        }

        .nav-item.active {
            background: linear-gradient(135deg, rgba(239, 246, 255, 0.9) 0%, rgba(219, 234, 254, 0.7) 100%);
            color: #2563EB;
            font-weight: 700;
            border: 1px solid rgba(191, 219, 254, 0.8);
            box-shadow: 0 2px 8px -2px rgba(37, 99, 235, 0.15);
        }
        .nav-item.active i {
            color: #2563EB;
        }

        .drag-overlay {
            display: none;
        }
        body.dragging .drag-overlay {
            display: flex;
        }
    """
    html = html[:old_style_match.start()] + f"<style>{enhanced_css}</style>" + html[old_style_match.end():]

# 3. Add Pin Toggle capability to sidebar
pin_toggle_btn = """                <!-- Brand Logo & Pin Toggle -->
                <div class="flex items-center justify-between mb-8 px-1">
                    <div class="flex items-center space-x-3 min-w-0">
                        <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-700 via-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-blue-500/25 shrink-0">
                            <i class="fa-solid fa-cube text-xl"></i>
                        </div>
                        <div class="sidebar-text overflow-hidden">
                            <h1 class="font-extrabold text-sm tracking-tight text-slate-900 leading-tight">Hưng Phát WMS</h1>
                            <span class="text-[10px] font-bold text-blue-600 uppercase tracking-wider">AI301 Đề 04</span>
                        </div>
                    </div>
                    <button onclick="toggleSidebarPin()" title="Ghim/Tháo ghim thanh công cụ" class="sidebar-text w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-xs transition-all cursor-pointer ml-auto">
                        <i class="fa-solid fa-chevron-left text-[10px]"></i>
                    </button>
                </div>"""

html = re.sub(
    r'<!-- Brand Logo \(Always Centered When Collapsed\) -->\s*<div class="flex items-center space-x-3 mb-8 px-1">.*?<\/div>\s*<\/div>',
    pin_toggle_btn,
    html,
    flags=re.DOTALL
)

# 4. Add JS function toggleSidebarPin
if "toggleSidebarPin" not in html:
    pin_js = """
        function toggleSidebarPin() {
            const sidebar = document.querySelector('aside.sidebar-collapsible');
            if (sidebar) {
                sidebar.classList.toggle('is-pinned');
            }
        }
    """
    html = html.replace("function switchTab(", pin_js + "\n        function switchTab(")

# Write to public/index.html and root dashboard
INDEX_HTML.write_text(html, encoding="utf-8")
ROOT_HTML.write_text(html, encoding="utf-8")
print("SUCCESS: Restored classic layout with polished visuals (Plus Jakarta Sans, frosted glass, rounded cards, animated sidebar)!")

