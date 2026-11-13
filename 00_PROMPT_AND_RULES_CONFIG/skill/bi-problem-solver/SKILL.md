---
name: bi-problem-solver
description: Universal Business Intelligence, data cleansing, problem discovery, root-cause workflow diagnostics, MCDA solution engineering, interactive HTML dashboards, and executive Word/PDF reporting.
---

# Universal BI & Strategic Problem Solver Skill

This skill equips Antigravity with the comprehensive methodology to:
1. Ingest, clean, and standardize multi-source data (Google Sheets, Lark Base, Excel, CSV) into a 10-sheet Native Pivot Table Excel workbook with cross-linked Slicers and standard accounting formats.
2. Conduct deep data auditing, identify operational anomalies, examine As-Is broken workflows (human manual errors, broken handoffs), and diagnose root causes via 5-Whys.
3. Engineer actionable To-Be solutions featuring Operational Gating Filters, MCDA scoring matrices, prioritized Pareto action plans, standalone interactive HTML dashboards, and executive Word/PDF reports.

## When to Use This Skill
- User provides any tabular dataset, Google Sheets URL, or Lark Base URL for analysis.
- User requests data cleaning, anomaly detection, or root-cause problem diagnosis.
- User requests building an Excel dashboard with Native Pivot Tables and Slicers.
- User asks for an interactive HTML executive dashboard or a managerial business report.

## Core Engines in Package
- `data_pipeline_engine.py`: Multi-source ingestion & 25-column data cleansing.
- `build_full_pivot_workbook.ps1`: 10-sheet Native Pivot Tables & Slicers builder (Run with `BypassSandbox: true`).
- `generate_html_dashboard.py` / `build_integrated_html.py`: Standalone Interactive HTML dashboard generator.
- `build_full_word_report.py`: 5-chapter executive Word report builder.
- `export_pdf_and_distribute.ps1`: Word to PDF vector converter.