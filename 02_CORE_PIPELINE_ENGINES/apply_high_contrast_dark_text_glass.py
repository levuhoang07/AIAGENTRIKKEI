# -*- coding: utf-8 -*-
"""
Apply High-Contrast Bold Black Text & Numbers on Luminous Frosted Glass:
- Preserves 100% of the Classic Dashboard Layout (4 Core Kanban Cards, All 5 Tabs, Header)
- Keeps Vibrant Purple-to-Magenta Gradient Background with Geometric Dot Matrix
- Upgrades Glass Cards to Luminous Frosted White Glass (rgba(255, 255, 255, 0.82) + blur(28px))
- Enhances ALL text and numbers to BOLD BLACK (#000000 / #0F172A) with heavy font weight
- Crystal-clear WCAG AAA readability on all metrics (4.70, 4.28, 713 Leads, 150.3 Tỷ đ, etc.)
- Chart.js defaults updated to dark bold text
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "public" / "index.html"
ROOT_HTML = BASE_DIR / "AI301_Executive_Integrated_Dashboard.html"

content = INDEX_HTML.read_text(encoding="utf-8")

# High-contrast bold dark text & numbers on luminous glass
high_contrast_glass_css = """
        :root {
            --glass-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.86) 0%, rgba(255, 255, 255, 0.74) 100%);
            --glass-bg-hover: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.84) 100%);
            --glass-border: rgba(255, 255, 255, 0.95);
            --glass-border-hover: rgba(59, 130, 246, 0.65);
            --glass-shadow: 0 16px 36px -8px rgba(35, 15, 60, 0.22), inset 0 1.5px 1.5px 0 rgba(255, 255, 255, 1), inset 0 -1px 1px 0 rgba(255, 255, 255, 0.4);
            --glass-shadow-hover: 0 24px 50px -10px rgba(35, 15, 60, 0.32), 0 0 0 1px rgba(59, 130, 246, 0.35), inset 0 2px 2px 0 rgba(255, 255, 255, 1);
        }

        body {
            /* Vibrant Royal Violet to Magenta Gradient with Geometric Dot Matrix Pattern */
            background: 
                radial-gradient(rgba(255, 255, 255, 0.18) 1.2px, transparent 1.2px),
                linear-gradient(135deg, #2b144e 0%, #441a66 25%, #6a2375 55%, #942b70 80%, #b23568 100%);
            background-size: 24px 24px, 100% 100%;
            background-attachment: fixed;
            color: #0F172A;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }

        /* Luminous Frosted White Glass Kanban Cards with Bold Black Text */
        .kanban-card {
            position: relative;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--glass-shadow) !important;
            border-radius: 1.5rem !important; /* Bo tròn 24px mềm mại */
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, background 0.3s ease;
            overflow: hidden;
            color: #0F172A !important;
        }
        .kanban-card:hover {
            transform: translateY(-5px) scale(1.008);
            box-shadow: var(--glass-shadow-hover) !important;
            border-color: var(--glass-border-hover) !important;
            background: var(--glass-bg-hover) !important;
        }
        /* Top Specular Sheen Bar */
        .kanban-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 38%;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0) 100%);
            border-top-left-radius: inherit;
            border-top-right-radius: inherit;
            pointer-events: none;
            z-index: 1;
        }
        .kanban-card > * {
            position: relative;
            z-index: 2;
        }

        /* BOLD BLACK TEXT & NUMBERS (ĐEN ĐẬM CHỮ VÀ SỐ CHO DỄ NHÌN) */
        .kanban-card h2,
        .kanban-card h3,
        .kanban-card h4,
        .kanban-card .font-extrabold,
        .kanban-card .font-bold {
            color: #0F172A !important;
            font-weight: 800 !important;
        }
        .kanban-card .text-slate-900,
        .kanban-card .text-slate-800,
        .kanban-card .text-slate-700 {
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        .kanban-card .text-slate-600,
        .kanban-card .text-slate-500 {
            color: #1E293B !important;
            font-weight: 600 !important;
        }
        .kanban-card .text-slate-400 {
            color: #334155 !important;
            font-weight: 600 !important;
        }

        /* ALL NUMBERS AND SCORES IN MAXIMUM CONTRAST BOLD BLACK */
        #kpi-top1-score,
        #kpi-top2-score,
        #kpi-budget-total,
        #kpi-retail-leads,
        #gauge-center-pct,
        .kanban-card .text-2xl,
        .kanban-card .text-3xl,
        .kanban-card .text-xl,
        .kanban-card .font-black {
            color: #000000 !important;
            font-weight: 900 !important;
            letter-spacing: -0.02em !important;
        }

        /* Inset Stats Boxes inside Cards */
        .kanban-card .bg-slate-50,
        .kanban-card .bg-slate-50\\/90,
        .kanban-card .bg-slate-100 {
            background: rgba(255, 255, 255, 0.72) !important;
            border: 1px solid rgba(203, 213, 225, 0.8) !important;
            backdrop-filter: blur(14px) !important;
            box-shadow: 0 2px 6px -1px rgba(15, 23, 42, 0.05), inset 0 1px 1px rgba(255, 255, 255, 0.95);
        }
        .kanban-card .border-slate-100,
        .kanban-card .border-slate-100\\/90,
        .kanban-card .border-slate-200 {
            border-color: rgba(203, 213, 225, 0.85) !important;
        }

        /* Progress Bar Comparison Labels in Bold Black */
        .kanban-card .font-mono {
            color: #000000 !important;
            font-weight: 800 !important;
        }
        .kanban-card .bg-slate-100 {
            background: rgba(226, 232, 240, 0.9) !important;
        }

        /* Header in Luminous Frosted Glass with Bold Black Typography */
        header {
            background: rgba(255, 255, 255, 0.88) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.95) !important;
            box-shadow: 0 8px 30px rgba(35, 15, 60, 0.15) !important;
        }
        header h2 {
            color: #0F172A !important;
            font-weight: 900 !important;
        }
        header p {
            color: #334155 !important;
            font-weight: 600 !important;
        }
        header input {
            background: rgba(248, 250, 252, 0.95) !important;
            border: 1px solid rgba(203, 213, 225, 0.9) !important;
            color: #0F172A !important;
            font-weight: 600 !important;
            box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.06) !important;
        }
        header input::placeholder {
            color: #64748B !important;
            font-weight: 500 !important;
        }

        /* Header Action Buttons */
        header .glass-btn-primary,
        header button[onclick*="file-uploader"] {
            background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.6) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }
        header .glass-btn-primary:hover,
        header button[onclick*="file-uploader"]:hover {
            background: linear-gradient(180deg, #1D4ED8 0%, #1E40AF 100%) !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45) !important;
        }
        header .glass-btn-secondary,
        header button[onclick*="exportToCSV"] {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(203, 213, 225, 0.9) !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
            color: #0F172A !important;
            font-weight: 800 !important;
        }
        header .glass-btn-secondary:hover,
        header button[onclick*="exportToCSV"]:hover {
            background: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1) !important;
        }

        /* Sidebar in Luminous Glass with Bold Dark Navigation */
        aside.sidebar-collapsible {
            width: 4.75rem; /* ~76px */
            transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease;
            will-change: width;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.88) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.95) !important;
            box-shadow: 10px 0 35px rgba(35, 15, 60, 0.15) !important;
        }
        aside.sidebar-collapsible:hover,
        aside.sidebar-collapsible.is-pinned {
            width: 17rem; /* ~272px */
            box-shadow: 14px 0 45px rgba(35, 15, 60, 0.22) !important;
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
        aside.sidebar-collapsible .nav-item {
            color: #334155 !important;
            font-weight: 700 !important;
        }
        aside.sidebar-collapsible .nav-item:hover {
            color: #0F172A !important;
            background: rgba(241, 245, 249, 0.9) !important;
        }
        aside.sidebar-collapsible .nav-item.active {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
            border: 1px solid #93C5FD !important;
            color: #1D4ED8 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
            font-weight: 800 !important;
        }
        aside.sidebar-collapsible .nav-item.active i {
            color: #1D4ED8 !important;
        }
        aside.sidebar-collapsible h1 {
            color: #0F172A !important;
            font-weight: 900 !important;
        }
        aside.sidebar-collapsible p {
            color: #475569 !important;
            font-weight: 700 !important;
        }

        /* Soft Rounded Glass Tables with Bold Dark Data */
        .table-rounded-container {
            border-radius: 1.5rem !important; /* Bo tròn 24px hoàn toàn */
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 16px 36px rgba(35, 15, 60, 0.18), inset 0 1px 1px rgba(255, 255, 255, 1) !important;
            background: rgba(255, 255, 255, 0.88) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        }
        .table-rounded-container table {
            border-collapse: separate;
            border-spacing: 0;
        }
        .table-rounded-container thead {
            background: rgba(241, 245, 249, 0.95) !important;
        }
        .table-rounded-container thead tr th {
            color: #0F172A !important;
            font-weight: 800 !important;
            border-bottom: 2px solid rgba(203, 213, 225, 0.9) !important;
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
        .table-rounded-container tbody tr {
            border-bottom: 1px solid rgba(226, 232, 240, 0.85) !important;
            color: #0F172A !important;
            transition: background-color 0.18s ease;
        }
        .table-rounded-container tbody tr:hover {
            background-color: rgba(239, 246, 255, 0.8) !important;
        }
        .table-rounded-container tbody td {
            color: #0F172A !important;
            font-weight: 600 !important;
        }
        .table-rounded-container tbody td.font-bold,
        .table-rounded-container tbody td.font-mono {
            color: #000000 !important;
            font-weight: 800 !important;
        }

        /* High-Contrast Badges */
        .badge-neon-emerald,
        .bg-emerald-50 {
            background: #ECFDF5 !important;
            border: 1px solid #6EE7B7 !important;
            color: #065F46 !important;
            font-weight: 800 !important;
        }
        .badge-neon-cyan,
        .bg-blue-50 {
            background: #EFF6FF !important;
            border: 1px solid #93C5FD !important;
            color: #1E40AF !important;
            font-weight: 800 !important;
        }
        .badge-neon-rose,
        .bg-red-50 {
            background: #FFF1F2 !important;
            border: 1px solid #FECDD3 !important;
            color: #9F1239 !important;
            font-weight: 800 !important;
        }
        .badge-neon-amber,
        .bg-amber-50 {
            background: #FFFBEB !important;
            border: 1px solid #FDE68A !important;
            color: #92400E !important;
            font-weight: 800 !important;
        }

        /* Minimalist Glass Dropzone */
        #empty-state-banner {
            background: rgba(255, 255, 255, 0.78) !important;
            border: 2px dashed rgba(59, 130, 246, 0.5) !important;
        }
        #empty-state-banner:hover {
            border-color: #2563EB !important;
            background: rgba(255, 255, 255, 0.92) !important;
        }
        #empty-state-banner h3 {
            color: #0F172A !important;
            font-weight: 900 !important;
        }
        #empty-state-banner p {
            color: #334155 !important;
            font-weight: 600 !important;
        }

        /* Active State Bar */
        #active-state-bar {
            background: rgba(236, 253, 245, 0.92) !important;
            border: 1px solid #6EE7B7 !important;
        }
        #active-state-bar span,
        #active-state-bar p {
            color: #064E3B !important;
            font-weight: 700 !important;
        }

        /* Modals in Clear Luminous Frosted Glass */
        #schema-modal > div > div,
        #error-modal > div > div {
            background: rgba(255, 255, 255, 0.96) !important;
            backdrop-filter: blur(32px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
            border: 1px solid rgba(203, 213, 225, 0.9) !important;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.35) !important;
            color: #0F172A !important;
        }
        #schema-modal h3, #error-modal h3 {
            color: #0F172A !important;
            font-weight: 900 !important;
        }
        #schema-modal p, #error-modal p {
            color: #334155 !important;
            font-weight: 600 !important;
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.6);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(100, 116, 139, 0.8);
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
content = style_pattern.sub(f"<style>{high_contrast_glass_css}    </style>", content)

# Update Chart.js defaults to dark bold text and clear gridlines
old_chart_defaults = re.compile(r'// Chart\.js.*?(?=function initCharts\(\))', re.DOTALL)
new_chart_defaults = """// Chart.js High Contrast Defaults
        if (window.Chart) {
            Chart.defaults.color = '#0F172A';
            Chart.defaults.borderColor = 'rgba(203, 213, 225, 0.6)';
            Chart.defaults.font.weight = 'bold';
        }
        """
content = old_chart_defaults.sub(new_chart_defaults, content)

# Write to public/index.html and root dashboard
INDEX_HTML.write_text(content, encoding="utf-8")
ROOT_HTML.write_text(content, encoding="utf-8")
print("SUCCESS: Applied High-Contrast Bold Black Text & Numbers on Luminous Frosted Glass!")
