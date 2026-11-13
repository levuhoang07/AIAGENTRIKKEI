# -*- coding: utf-8 -*-
"""
Apply Ultra-Glossy Purple/Magenta Liquid Glassmorphism Theme (from media_1794582215684_90fe0bd0.jpg)
- Preserves 100% of the Classic Dashboard Layout (4 Core Kanban Cards, All 5 Tabs, Header)
- Vibrant Royal Violet to Magenta Mesh Gradient with subtle geometric dot-matrix pattern
- Ultra-Realistic Liquid Glassmorphism (specular sheen, inset reflection, 24px rounded corners)
- Glowing neon accents (cyan, emerald, fuchsia, amber) for KPI badges and charts
- High-contrast crisp typography (Plus Jakarta Sans)
- Chart.js defaults configured for glowing dark neon glass
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = BASE_DIR / "public" / "index.html"
ROOT_HTML = BASE_DIR / "AI301_Executive_Integrated_Dashboard.html"

content = INDEX_HTML.read_text(encoding="utf-8")

# Ultra-Glossy Glassmorphic CSS matching the reference image
ultra_gloss_css = """
        :root {
            --glass-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.06) 100%);
            --glass-bg-hover: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.10) 100%);
            --glass-border: rgba(255, 255, 255, 0.35);
            --glass-border-hover: rgba(255, 255, 255, 0.65);
            --glass-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.45), inset 0 1.5px 1.5px 0 rgba(255, 255, 255, 0.75), inset 0 -1px 1px 0 rgba(255, 255, 255, 0.15);
            --glass-shadow-hover: 0 28px 60px -10px rgba(0, 0, 0, 0.55), inset 0 2px 2px 0 rgba(255, 255, 255, 0.95), inset 0 -1px 1px 0 rgba(255, 255, 255, 0.25);
        }

        body {
            /* Vibrant Royal Violet to Magenta Gradient with Geometric Dot Matrix Pattern (Exact Reference UI Kit) */
            background: 
                radial-gradient(rgba(255, 255, 255, 0.18) 1.2px, transparent 1.2px),
                linear-gradient(135deg, #2b144e 0%, #441a66 25%, #6a2375 55%, #942b70 80%, #b23568 100%);
            background-size: 24px 24px, 100% 100%;
            background-attachment: fixed;
            color: #FFFFFF;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }

        /* Ultra-Glossy Glassmorphic Kanban Cards with Specular Highlight Reflection */
        .kanban-card {
            position: relative;
            background: var(--glass-bg) !important;
            backdrop-filter: blur(24px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--glass-shadow) !important;
            border-radius: 1.5rem !important; /* Bo tròn 24px mềm mại */
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, background 0.3s ease;
            overflow: hidden;
        }
        .kanban-card:hover {
            transform: translateY(-5px) scale(1.008);
            box-shadow: var(--glass-shadow-hover) !important;
            border-color: var(--glass-border-hover) !important;
            background: var(--glass-bg-hover) !important;
        }
        /* Top Specular Sheen Bar (Bóng sáng phản chiếu của kính chất lỏng) */
        .kanban-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 38%;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0) 100%);
            border-top-left-radius: inherit;
            border-top-right-radius: inherit;
            pointer-events: none;
            z-index: 1;
        }
        .kanban-card > * {
            position: relative;
            z-index: 2;
        }

        /* Glass Text Color Overrides for High Contrast */
        .kanban-card .text-slate-900,
        .kanban-card .text-slate-800,
        .kanban-card .text-slate-700 {
            color: #FFFFFF !important;
        }
        .kanban-card .text-slate-600,
        .kanban-card .text-slate-500,
        .kanban-card .text-slate-400 {
            color: rgba(255, 255, 255, 0.75) !important;
        }

        /* Inset Frosted Glass Stats Boxes */
        .kanban-card .bg-slate-50,
        .kanban-card .bg-slate-50\\/90,
        .kanban-card .bg-slate-100 {
            background: rgba(255, 255, 255, 0.09) !important;
            border-color: rgba(255, 255, 255, 0.18) !important;
            backdrop-filter: blur(14px) !important;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.35);
        }
        .kanban-card .border-slate-100,
        .kanban-card .border-slate-100\\/90,
        .kanban-card .border-slate-200 {
            border-color: rgba(255, 255, 255, 0.18) !important;
        }

        /* Header in Translucent Frosted Glass */
        header {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(28px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(200%) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.20) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25) !important;
        }
        header h2 {
            color: #FFFFFF !important;
        }
        header p {
            color: rgba(255, 255, 255, 0.75) !important;
        }
        header input {
            background: rgba(0, 0, 0, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: #FFFFFF !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.35) !important;
        }
        header input::placeholder {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        header input:focus {
            background: rgba(0, 0, 0, 0.35) !important;
            border-color: rgba(255, 255, 255, 0.6) !important;
        }

        /* Glossy Pill Action Buttons (Matches UI Kit "LOGIN IN", "CONTACT", "DOWNLOAD") */
        .glass-btn-primary {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.38) 0%, rgba(255, 255, 255, 0.12) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.55) !important;
            box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 8px 20px rgba(0, 0, 0, 0.3) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            backdrop-filter: blur(16px) !important;
            transition: all 0.25s ease !important;
        }
        .glass-btn-primary:hover {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.52) 0%, rgba(255, 255, 255, 0.20) 100%) !important;
            border-color: rgba(255, 255, 255, 0.85) !important;
            box-shadow: inset 0 1.5px 2px rgba(255, 255, 255, 1), 0 12px 25px rgba(0, 0, 0, 0.4) !important;
            transform: translateY(-2px);
        }

        .glass-btn-secondary {
            background: rgba(255, 255, 255, 0.12) !important;
            border: 1px solid rgba(255, 255, 255, 0.32) !important;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.5), 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            backdrop-filter: blur(16px) !important;
            transition: all 0.25s ease !important;
        }
        .glass-btn-secondary:hover {
            background: rgba(255, 255, 255, 0.22) !important;
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.8), 0 8px 20px rgba(0, 0, 0, 0.3) !important;
            transform: translateY(-2px);
        }

        /* Collapsible Smooth Animated Sidebar (Mở ra khi di chuột, đóng lại bình thường) */
        aside.sidebar-collapsible {
            width: 4.75rem; /* ~76px */
            transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease;
            will-change: width;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(28px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(200%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.18) !important;
            box-shadow: 12px 0 35px rgba(0, 0, 0, 0.3) !important;
        }
        aside.sidebar-collapsible:hover,
        aside.sidebar-collapsible.is-pinned {
            width: 17rem; /* ~272px */
            box-shadow: 16px 0 45px rgba(0, 0, 0, 0.45) !important;
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
            color: rgba(255, 255, 255, 0.75) !important;
        }
        aside.sidebar-collapsible .nav-item:hover {
            color: #FFFFFF !important;
            background: rgba(255, 255, 255, 0.12) !important;
        }
        aside.sidebar-collapsible .nav-item.active {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.32) 0%, rgba(255, 255, 255, 0.12) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.55) !important;
            color: #FFFFFF !important;
            box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.8), 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            font-weight: 700;
        }
        aside.sidebar-collapsible .nav-item.active i {
            color: #FFFFFF !important;
        }
        aside.sidebar-collapsible h1 {
            color: #FFFFFF !important;
        }

        /* Soft Rounded Glass Tables with Zero Sharp Edges */
        .table-rounded-container {
            border-radius: 1.5rem !important; /* Bo tròn 24px hoàn toàn */
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.6) !important;
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(24px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
        }
        .table-rounded-container table {
            border-collapse: separate;
            border-spacing: 0;
        }
        .table-rounded-container thead {
            background: rgba(255, 255, 255, 0.14) !important;
        }
        .table-rounded-container thead tr th {
            color: #FFFFFF !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.18) !important;
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
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: rgba(255, 255, 255, 0.92) !important;
            transition: background-color 0.18s ease;
        }
        .table-rounded-container tbody tr:hover {
            background-color: rgba(255, 255, 255, 0.14) !important;
        }
        .table-rounded-container tbody td {
            color: rgba(255, 255, 255, 0.92) !important;
        }

        /* Glowing Neon Glass Badges */
        .badge-neon-emerald {
            background: rgba(16, 185, 129, 0.25) !important;
            border: 1px solid rgba(52, 211, 153, 0.5) !important;
            color: #6EE7B7 !important;
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.25);
        }
        .badge-neon-cyan {
            background: rgba(56, 189, 248, 0.25) !important;
            border: 1px solid rgba(56, 189, 248, 0.5) !important;
            color: #BAE6FD !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }
        .badge-neon-rose {
            background: rgba(244, 63, 94, 0.25) !important;
            border: 1px solid rgba(251, 113, 133, 0.5) !important;
            color: #FECDD3 !important;
            box-shadow: 0 0 12px rgba(244, 63, 94, 0.25);
        }
        .badge-neon-amber {
            background: rgba(245, 158, 11, 0.25) !important;
            border: 1px solid rgba(251, 191, 36, 0.5) !important;
            color: #FDE68A !important;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.25);
        }

        /* Minimalist Glass Dropzone */
        #empty-state-banner {
            border: 2px dashed rgba(255, 255, 255, 0.35) !important;
        }
        #empty-state-banner:hover {
            border-color: rgba(56, 189, 248, 0.8) !important;
            background: rgba(255, 255, 255, 0.12) !important;
        }

        /* Active State Bar */
        #active-state-bar {
            background: rgba(16, 185, 129, 0.18) !important;
            border: 1px solid rgba(52, 211, 153, 0.45) !important;
        }

        /* Modals in Dark Glassmorphism */
        #schema-modal > div > div,
        #error-modal > div > div {
            background: linear-gradient(135deg, rgba(35, 20, 60, 0.95) 0%, rgba(55, 25, 80, 0.95) 100%) !important;
            backdrop-filter: blur(32px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
            border: 1px solid rgba(255, 255, 255, 0.35) !important;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6), inset 0 1.5px 1.5px rgba(255, 255, 255, 0.6) !important;
            color: #FFFFFF !important;
        }
        #schema-modal h3, #error-modal h3 {
            color: #FFFFFF !important;
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
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
content = style_pattern.sub(f"<style>{ultra_gloss_css}    </style>", content)

# Update buttons in header to have glass classes
content = content.replace(
    'class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-full text-xs font-bold shadow-md shadow-blue-500/20 hover:shadow-lg hover:shadow-blue-500/30 transition-all flex items-center space-x-1.5 shrink-0 cursor-pointer"',
    'class="glass-btn-primary px-5 py-2 rounded-full text-xs font-bold transition-all flex items-center space-x-1.5 shrink-0 cursor-pointer"'
)
content = content.replace(
    'class="bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 px-3.5 py-2 rounded-full text-xs font-bold shadow-2xs transition-all flex items-center space-x-1.5 shrink-0 cursor-pointer"',
    'class="glass-btn-secondary px-3.5 py-2 rounded-full text-xs font-bold transition-all flex items-center space-x-1.5 shrink-0 cursor-pointer"'
)

# Update Chart.js defaults to glowing light text and borders
chart_defaults = """
        // Chart.js Ultra-Glossy Theme Defaults
        if (window.Chart) {
            Chart.defaults.color = 'rgba(255, 255, 255, 0.75)';
            Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.12)';
        }
"""
if "Chart.defaults.color" not in content:
    content = content.replace("function initCharts() {", chart_defaults + "\n        function initCharts() {")

# Write to public/index.html and root dashboard
INDEX_HTML.write_text(content, encoding="utf-8")
ROOT_HTML.write_text(content, encoding="utf-8")
print("SUCCESS: Ultra-Glossy Purple/Magenta Liquid Glass Theme applied while preserving 100% of the classic 4-card layout!")
