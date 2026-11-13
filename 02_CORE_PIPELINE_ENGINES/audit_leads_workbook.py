"""Audit lead-level evidence in the AI301 cleaned workbook."""
import argparse
from collections import Counter, defaultdict
from hashlib import file_digest
import json
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


def collect_workbook(path):
    with path.open("rb") as stream:
        digest = file_digest(stream, "sha256").hexdigest()
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = next(sheet for sheet in workbook if sheet.title.strip() == "Dữ liệu nguồn")
        rows = sheet.values
        headers = next(rows)
        groups = defaultdict(list)
        for number, values in enumerate(rows, 2):
            row = dict(zip(headers, values))
            if row["Mã Hồ Sơ"]:
                groups[row["Mã Địa Bàn"]].append((number, row))
        if len(groups) != 4 or None in groups:
            raise ValueError("Cần đúng bốn mã địa bàn")
        fields = ["Độ Tương Thích Sản Phẩm", "Khả Năng Đáp Ứng của Hưng Phát",
                  "Kỳ Thống Kê", "Trùng Lặp Nguồn", "Nguồn Tài Liệu Dữ Liệu"]
        result = {}
        for area, records in sorted(groups.items()):
            result[area] = {
                "leads": len(records),
                "retail_groups": Counter(row["Mô Hình Bán Lẻ"] for _, row in records
                                         if row["Mô Hình Bán Lẻ"]),
                "distributions": {field: Counter(row[field] or "Thiếu" for _, row in records)
                                  for field in fields},
                "source_rows": [number for number, _ in records],
                "repeated_record_ids": sum(n - 1 for n in Counter(
                    row["Mã Hồ Sơ"] for _, row in records).values()),
            }
        mcda = {}
        if "Ma Trận MCDA" in workbook.sheetnames:
            score_sheet = workbook["Ma Trận MCDA"]
            for number, values in enumerate(score_sheet.iter_rows(min_row=4, max_col=8, values_only=True), 4):
                area = values[0]
                if area not in result:
                    continue
                if area in mcda:
                    raise ValueError(f"Nhiều dòng điểm MCDA cho {area}")
                mcda[area] = {
                    key: {"value": values[column - 1],
                          "cell": f"'{score_sheet.title}'!{get_column_letter(column)}{number}"}
                    for column, key in enumerate(("fit", "deployment", "competition", "scale", "total", "decision"), 3)
                }
        plans = defaultdict(list)
        if "Kế Hoạch Khảo Sát" in workbook.sheetnames:
            plan_sheet = workbook["Kế Hoạch Khảo Sát"]
            for number, values in enumerate(plan_sheet.iter_rows(min_row=4, max_col=8, values_only=True), 4):
                record_id, area = values[:2]
                if record_id and area in result:
                    matches = [(source_row, row) for source_row, row in groups[area]
                               if row["Mã Hồ Sơ"] == record_id]
                    group = matches[0][1]["Mô Hình Bán Lẻ"] if len(matches) == 1 else None
                    plans[area].append({"record_id": record_id, "group": group,
                                        "cell": f"'{plan_sheet.title}'!A{number}",
                                        "source_rows": [source_row for source_row, _ in matches]})
        recorded_priority = {}
        for area, scores in mcda.items():
            decision = scores["decision"]["value"]
            if not isinstance(decision, str):
                continue
            for rank in (1, 2):
                if decision.strip().upper().startswith(f"HẠNG {rank} -"):
                    recorded_priority.setdefault(rank, []).append(area)
        proposed = [recorded_priority[rank][0] for rank in (1, 2)] if all(
            len(recorded_priority.get(rank, [])) == 1 for rank in (1, 2)
        ) else []
        evidence = {"source": str(path.resolve()), "sha256": digest, "sheet": sheet.title,
                    "areas": result, "status": "needs_rules_and_evidence",
                    "recorded_mcda": mcda,
                    "recorded_proposal": proposed, "recorded_survey": dict(plans),
                    "survey_status": "incomplete" if proposed else "pending_selection",
                    "selected": [], "required": [
                        "Xác nhận cách tính điểm từng tiêu chí và điều kiện sàng lọc",
                        "Bổ sung căn cứ cạnh tranh và xác nhận năng lực triển khai theo địa bàn",
                        "Xác nhận quy tắc xử lý kỳ khác nhau và nguồn lặp",
                    ]}
    finally:
        workbook.close()
    return evidence


def run(path, output):
    evidence = collect_workbook(path)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.suffix.lower() != ".json" or args.output.exists():
        parser.error("Chọn một tệp kết quả JSON mới")
    run(args.input, args.output)
