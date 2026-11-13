# -*- coding: utf-8 -*-
"""
Fine-tune Kanban Cards Transparency:
- Reduces white opacity from ~0.86 to a balanced frosted glass ~0.45 - 0.30
- Background purple-to-magenta gradient & dot matrix shines through with rich depth
- Retains BOLD BLACK text & numbers (#000000 / #0F172A) with soft text highlight for 100% readability
- Inner stat boxes, tables, header, and sidebar calibrated for cohesive glassmorphism
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "public" / "index.html"
ROOT_HTML = BASE_DIR / "AI301_Executive_Integrated_Dashboard.html"

content = INDEX_HTML.read_text(encoding="utf-8")

# Translucent Glass CSS
calibrated_glass_css = """
        :root {
            /* Balanced Translucent Frosted Glass (Không bị quá trắng, trong suốt phản chiếu nền) */
            --glass-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.50) 0%, rgba(255, 255, 255, 0.30) 100%);
            --glass-bg-hover: linear-gradient(135deg, rgba(255, 255, 255, 0.62) 0%, rgba(255, 255, 255, 0.40) 100%);
            --glass-border: rgba(255, 255, 255, 0.60);
            --glass-border-hover: rgba(255, 255, 255, 0.85);
            --glass-shadow: 0 16px 40px -10px rgba(25, 10, 45, 0.30), inset 0 1.5px 1.5px 0 rgba(255, 255, 255, 0.75), inset 0 -1px 1px 0 rgba(255, 255, 255, 0.25);
            --glass-shadow-hover: 0 24px 50px -10px rgba(25, 10, 45, 0.40), 0 0 0 1px rgba(255, 255, 255, 0.5), inset 0 2px 2px 0 rgba(255, 255, 255, 0.9);
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

        /* Translucent Frosted Glass Kanban Cards */
        .kanban-card {
            position: relative;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(24px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(190%) !important;
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
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0) 100%);
            border-top-left-radius: inherit;
            border-top-right-radius: inherit;
            pointer-events: none;
            z-index: 1;
        }
        .kanban-card > * {
            position: relative;
            z-index: 2;
        }

        /* BOLD BLACK TEXT & NUMBERS (ĐEN ĐẬM DỄ ĐỌC TRÊN NỀN KÍNH TRONG SUỐT) */
        .kanban-card h2,
        .kanban-card h3,
        .kanban-card h4,
        .kanban-card .font-extrabold,
        .kanban-card .font-bold {
            color: #000000 !important;
            font-weight: 800 !important;
            text-shadow: 0 1px 1px rgba(255, 255, 255, 0.4);
        }
        .kanban-card .text-slate-900,
        .kanban-card .text-slate-800,
        .kanban-card .text-slate-700 {
            color: #0F172A !important;
            font-weight: 700 !important;
            text-shadow: 0 1px 1px rgba(255, 255, 255, 0.35);
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
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
        }

        /* Inset Frosted Stats Boxes inside Cards (Trong suốt nhẹ nhàng) */
        .kanban-card .bg-slate-50,
        .kanban-card .bg-slate-50\\/90,
        .kanban-card .bg-slate-100 {
            background: rgba(255, 255, 255, 0.38) !important;
            border: 1px solid rgba(255, 255, 255, 0.50) !important;
            backdrop-filter: blur(14px) !important;
            box-shadow: 0 2px 8px -1px rgba(25, 10, 45, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.7);
        }
        .kanban-card .border-slate-100,
        .kanban-card .border-slate-100\\/90,
        .kanban-card .border-slate-200 {
            border-color: rgba(255, 255, 255, 0.50) !important;
        }

        /* Progress Bar Comparison Labels in Bold Black */
        .kanban-card .font-mono {
            color: #000000 !important;
            font-weight: 800 !important;
        }
        .kanban-card .bg-slate-100 {
            background: rgba(255, 255, 255, 0.35) !important;
        }

        /* Header in Translucent Frosted Glass */
        header {
            background: rgba(255, 255, 255, 0.55) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.65) !important;
            box-shadow: 0 8px 30px rgba(25, 10, 45, 0.20) !important;
        }
        header h2 {
            color: #000000 !important;
            font-weight: 900 !important;
            text-shadow: 0 1px 1px rgba(255, 255, 255, 0.4);
        }
        header p {
            color: #1E293B !important;
            font-weight: 600 !important;
        }
        header input {
            background: rgba(255, 255, 255, 0.55) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important;
            color: #000000 !important;
            font-weight: 700 !important;
            box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.08) !important;
        }
        header input::placeholder {
            color: #475569 !important;
            font-weight: 600 !important;
        }

        /* Header Action Buttons */
        header .glass-btn-primary,
        header button[onclick*="file-uploader"] {
            background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.7) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }
        header .glass-btn-primary:hover,
        header button[onclick*="file-uploader"]:hover {
            background: linear-gradient(180deg, #1D4ED8 0%, #1E40AF 100%) !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5) !important;
        }
        header .glass-btn-secondary,
        header button[onclick*="exportToCSV"] {
            background: rgba(255, 255, 255, 0.60) !important;
            border: 1px solid rgba(255, 255, 255, 0.75) !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.8) !important;
            color: #000000 !important;
            font-weight: 800 !important;
        }
        header .glass-btn-secondary:hover,
        header button[onclick*="exportToCSV"]:hover {
            background: rgba(255, 255, 255, 0.80) !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12) !important;
        }

        /* Sidebar in Translucent Glass */
        aside.sidebar-collapsible {
            width: 4.75rem; /* ~76px */
            transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease;
            will-change: width;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.55) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.65) !important;
            box-shadow: 10px 0 35px rgba(25, 10, 45, 0.20) !important;
        }
        aside.sidebar-collapsible:hover,
        aside.sidebar-collapsible.is-pinned {
            width: 17rem; /* ~272px */
            box-shadow: 14px 0 45px rgba(25, 10, 45, 0.30) !important;
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
            color: #1E293B !important;
            font-weight: 700 !important;
        }
        aside.sidebar-collapsible .nav-item:hover {
            color: #000000 !important;
            background: rgba(255, 255, 255, 0.45) !important;
        }
        aside.sidebar-collapsible .nav-item.active {
            background: rgba(255, 255, 255, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            color: #1D4ED8 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.18), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
            font-weight: 800 !important;
        }
        aside.sidebar-collapsible .nav-item.active i {
            color: #1D4ED8 !important;
        }
        aside.sidebar-collapsible h1 {
            color: #000000 !important;
            font-weight: 900 !important;
        }
        aside.sidebar-collapsible p {
            color: #334155 !important;
            font-weight: 700 !important;
        }

        /* Translucent Glass Tables */
        .table-rounded-container {
            border-radius: 1.5rem !important; /* Bo tròn 24px hoàn toàn */
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.65) !important;
            box-shadow: 0 16px 36px rgba(25, 10, 45, 0.22), inset 0 1px 1px rgba(255, 255, 255, 0.8) !important;
            background: rgba(255, 255, 255, 0.52) !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        }
        .table-rounded-container table {
            border-collapse: separate;
            border-spacing: 0;
        }
        .table-rounded-container thead {
            background: rgba(255, 255, 255, 0.45) !important;
        }
        .table-rounded-container thead tr th {
            color: #000000 !important;
            font-weight: 800 !important;
            border-bottom: 2px solid rgba(255, 255, 255, 0.6) !important;
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
            border-bottom: 1px solid rgba(255, 255, 255, 0.35) !important;
            color: #0F172A !important;
            transition: background-color 0.18s ease;
        }
        .table-rounded-container tbody tr:hover {
            background-color: rgba(255, 255, 255, 0.35) !important;
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
            background: rgba(209, 250, 229, 0.85) !important;
            border: 1px solid #34D399 !important;
            color: #064E3B !important;
            font-weight: 800 !important;
        }
        .badge-neon-cyan,
        .bg-blue-50 {
            background: rgba(219, 234, 254, 0.85) !important;
            border: 1px solid #60A5FA !important;
            color: #1E3A8A !important;
            font-weight: 800 !important;
        }
        .badge-neon-rose,
        .bg-red-50 {
            background: rgba(255, 228, 230, 0.85) !important;
            border: 1px solid #FB7185 !important;
            color: #881337 !important;
            font-weight: 800 !important;
        }
        .badge-neon-amber,
        .bg-amber-50 {
            background: rgba(254, 243, 199, 0.85) !important;
            border: 1px solid #FBBF24 !important;
            color: #78350F !important;
            font-weight: 800 !important;
        }

        /* Minimalist Glass Dropzone */
        #empty-state-banner {
            background: rgba(255, 255, 255, 0.45) !important;
            border: 2px dashed rgba(255, 255, 255, 0.7) !important;
        }
        #empty-state-banner:hover {
            border-color: #2563EB !important;
            background: rgba(255, 255, 255, 0.65) !important;
        }
        #empty-state-banner h3 {
            color: #000000 !important;
            font-weight: 900 !important;
        }
        #empty-state-banner p {
            color: #1E293B !important;
            font-weight: 600 !important;
        }

        /* Active State Bar */
        #active-state-bar {
            background: rgba(209, 250, 229, 0.85) !important;
            border: 1px solid #34D399 !important;
        }
        #active-state-bar span,
        #active-state-bar p {
            color: #064E3B !important;
            font-weight: 800 !important;
        }

        /* Modals in Balanced Frosted Glass */
        #schema-modal > div > div,
        #error-modal > div > div {
            background: rgba(255, 255, 255, 0.90) !important;
            backdrop-filter: blur(32px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.35) !important;
            color: #0F172A !important;
        }
        #schema-modal h3, #error-modal h3 {
            color: #000000 !important;
            font-weight: 900 !important;
        }
        #schema-modal p, #error-modal p {
            color: #1E293B !important;
            font-weight: 600 !important;
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.5);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.8);
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
content = style_pattern.sub(f"<style>{calibrated_glass_css}    </style>", content)

# Write to public/index.html and root dashboard
INDEX_HTML.write_text(content, encoding="utf-8")
ROOT_HTML.write_text(content, encoding="utf-8")
print("SUCCESS: Calibrated Kanban Cards to a balanced, gorgeous translucency!")
