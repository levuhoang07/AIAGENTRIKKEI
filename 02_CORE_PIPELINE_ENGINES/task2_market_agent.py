"""Local rule-based market evaluation workflow. Python 3.10+, standard library."""

import argparse
import hashlib
import json
import math
from pathlib import Path


KINDS = {"market", "competitor", "feedback", "product", "capacity"}


def read_json(path, trace):
    data = path.read_bytes()
    trace.append({"action": "read", "path": str(path),
                  "sha256": hashlib.sha256(data).hexdigest()})
    return json.loads(data.decode("utf-8-sig"))


def collect(root, bundle, metrics, trace):
    areas = bundle["areas"]
    if len(areas) != 4 or len(set(areas)) != 4 or not all(
        isinstance(area, str) and area.strip() for area in areas
    ):
        raise ValueError("Exactly four distinct area IDs are required")
    facts = {area: {metric: {} for metric in metrics} for area in areas}
    seen_kinds = {area: set() for area in areas}
    for filename in dict.fromkeys(bundle["documents"]):
        path = (root / filename).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Document must be inside the input directory")
        for index, row in enumerate(read_json(path, trace), 1):
            area, kind = row["area"], row["kind"]
            if area not in facts or kind not in KINDS:
                raise ValueError(f"Unknown area or document kind in {filename}#{index}")
            source, period, locator = (row[key] for key in ("source", "period", "locator"))
            if not all(isinstance(item, str) and item.strip() for item in (source, period, locator)):
                raise ValueError(f"Missing provenance in {filename}#{index}")
            seen_kinds[area].add(kind)
            for metric, observation in row.get("metrics", {}).items():
                rule = metrics.get(metric)
                if not rule or kind not in rule["kinds"]:
                    continue
                if observation["unit"] != rule["unit"] or period != rule["period"]:
                    trace.append({"action": "exclude_observation", "area": area, "metric": metric,
                                  "reason": "unit_or_period_mismatch", "file": filename, "record": index})
                    continue
                value = observation["value"]
                if type(value) not in (int, float) or not math.isfinite(value):
                    raise ValueError(f"Invalid numeric value in {filename}#{index}")
                evidence = {"value": value, "source": source, "period": period,
                            "locator": locator, "file": filename, "record": index}
                key = (source, period, value)
                if key in facts[area][metric]:
                    trace.append({"action": "duplicate", "area": area, "metric": metric,
                                  "evidence": evidence})
                else:
                    facts[area][metric][key] = evidence
    return facts, seen_kinds


def evaluate(facts, seen_kinds, rules):
    comparisons = []
    for area, metrics in facts.items():
        checks = []
        for metric, observations in metrics.items():
            rule = rules[metric]
            evidence = list(observations.values())
            values = {item["value"] for item in evidence}
            status, points = "missing", None
            if len(values) > 1:
                status = "conflict"
            elif values:
                value = next(iter(values))
                passed = value >= rule["threshold"] if rule["operator"] == ">=" else value <= rule["threshold"]
                status = "pass" if passed else "fail"
                points = rule["weight"] if passed else 0
            checks.append({"metric": metric, "status": status, "points": points,
                           "evidence": evidence, "rule": rule})
        missing_kinds = sorted(KINDS - seen_kinds[area])
        unresolved = missing_kinds or any(check["points"] is None for check in checks)
        excluded = any(check["status"] == "fail" and check["rule"].get("gate") for check in checks)
        status = "excluded" if excluded else "review" if unresolved else "eligible"
        comparisons.append({"area": area, "status": status, "checks": checks,
                            "missing_kinds": missing_kinds,
                            "score": None if unresolved else sum(check["points"] for check in checks)})
    eligible = sorted((row for row in comparisons if row["status"] == "eligible"),
                      key=lambda row: row["score"], reverse=True)
    blockers = []
    for row in comparisons:
        if row["status"] != "review":
            continue
        area = row["area"]
        for kind in row["missing_kinds"]:
            blockers.append(f"{area} — Bổ sung nhóm hồ sơ {kind}.")
        for check in row["checks"]:
            rule = check["rule"]
            if check["status"] == "missing":
                blockers.append(f"{area} — Bổ sung {check['metric']} cho kỳ {rule['period']}, đơn vị {rule['unit']}.")
            if check["status"] == "conflict":
                blockers.append(f"{area} — Đối chiếu nguồn có giá trị mâu thuẫn cho {check['metric']} kỳ {rule['period']}.")
    if len(eligible) < 2:
        blockers.append("Fewer than two eligible areas. Verify evidence or deployment capacity.")
    if len(eligible) > 2 and eligible[1]["score"] == eligible[2]["score"]:
        blockers.append("Tie at the selection boundary. Business Development must resolve it.")
    selected = [] if blockers else [row["area"] for row in eligible[:2]]
    return comparisons, selected, blockers


def report(comparisons, selected, blockers, survey):
    lines = ["# Đề xuất khảo sát thị trường", "", "Kính gửi Trưởng phòng Phát triển Kinh doanh", "",
             "Địa bàn đề xuất — " + (", ".join(selected) or "Chưa đủ căn cứ để đề xuất hai địa bàn"), "",
             "## Bảng so sánh", "",
             "| Địa bàn | Tiêu chí | Dữ kiện gốc và căn cứ | Quy tắc | Đánh giá của Agent | Điểm |",
             "|---|---|---|---|---|---|"]
    for row in comparisons:
        for check in row["checks"]:
            rule = check["rule"]
            evidence = "; ".join(
                f"{item['value']} {rule['unit']} ({item['source']}, {item['period']}, "
                f"{item['locator']}, {item['file']}#{item['record']})"
                for item in check["evidence"]
            ) or "Chưa có dữ kiện phù hợp"
            cells = (row["area"], check["metric"], evidence,
                     f"{rule['operator']} {rule['threshold']}", check["status"], check["points"])
            lines.append("| " + " | ".join(str(cell).replace("|", r"\|").replace("\n", " ")
                                            for cell in cells) + " |")
    lines += ["", "## Căn cứ ưu tiên", ""]
    for row in comparisons:
        area = row["area"]
        status = row["status"]
        reason = {
            "excluded": "Không đạt điều kiện bắt buộc",
            "review": "Cần kiểm tra dữ kiện thiếu hoặc mâu thuẫn",
            "eligible": ("Thuộc hai địa bàn đủ điều kiện có điểm cao nhất" if area in selected else
                         "Điểm thấp hơn nhóm ưu tiên" if selected else "Chờ xử lý điều kiện quyết định"),
        }[status]
        missing = ", ".join(row["missing_kinds"])
        score = row["score"] if row["score"] is not None else "chưa xác định"
        lines.append(f"- {area} — {reason}. Điểm {score}." + (f" Thiếu nhóm hồ sơ {missing}." if missing else ""))
    lines += ["", "## Điểm cần con người xử lý", ""]
    lines += [f"- {item}" for item in blockers]
    lines += ["- Trưởng phòng Phát triển Kinh doanh kiểm tra căn cứ và duyệt kế hoạch trước khi tiếp cận khách hàng.",
              "", "## Kế hoạch khảo sát", ""]
    for area in selected:
        plan = survey.get(area, {})
        for key, label in (("group", "Nhóm khách"), ("verify", "Thông tin cần xác minh"), ("owner", "Phụ trách")):
            lines.append(f"- {area} — {label} — {plan.get(key) or 'Cần Trưởng phòng xác nhận'}")
    if not selected:
        lines.append("Chờ xác minh các điều kiện quyết định trước khi lập danh sách tiếp cận.")
    return "\n".join(lines) + "\n"


def run(input_dir, rules_path, output):
    root = input_dir.resolve()
    output = output.resolve()
    if output.is_relative_to(root):
        raise ValueError("Output must be outside the input directory")
    output.mkdir(parents=True, exist_ok=False)
    trace = []
    try:
        bundle = read_json(root / "manifest.json", trace)
        config = read_json(rules_path, trace)
        rules = config["metrics"]
        if not rules or any(
            rule["operator"] not in (">=", "<=")
            or not set(rule["kinds"]) or not set(rule["kinds"]) <= KINDS
            or not math.isfinite(rule["weight"]) or rule["weight"] <= 0
            or not math.isfinite(rule["threshold"])
            for rule in rules.values()
        ):
            raise ValueError("Invalid metric rules")
        trace.append({"action": "call", "tool": "collect"})
        facts, seen_kinds = collect(root, bundle, rules, trace)
        trace.append({"action": "complete", "tool": "collect"})
        trace.append({"action": "call", "tool": "evaluate"})
        comparison, selected, blockers = evaluate(facts, seen_kinds, rules)
        trace.append({"action": "complete", "tool": "evaluate", "selected": selected})
        result = {"rule_version": config["version"], "areas": comparison,
                  "selected": selected, "review": blockers}
        survey = config["survey"]
        missing_survey = {
            area: [key for key in ("group", "verify", "owner") if not survey.get(area, {}).get(key)]
            for area in selected
        }
        missing_survey = {area: fields for area, fields in missing_survey.items() if fields}
        result["survey_status"] = ("pending_selection" if not selected else
                                   "incomplete" if missing_survey else "complete")
        result["missing_survey_fields"] = missing_survey
        text = report(comparison, selected, blockers, survey)
        if missing_survey:
            text += "\n**Kế hoạch chưa hoàn tất.**\n" + "\n".join(
                f"- {area} — Cần bổ sung {', '.join(fields)}." for area, fields in missing_survey.items()
            ) + "\n"
        (output / "report.md").write_text(text, encoding="utf-8")
        (output / "comparison.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        trace.append({"action": "success", "outputs": ["report.md", "comparison.json"]})
        return result
    except Exception as error:
        trace.append({"action": "failure", "error": str(error)})
        raise
    finally:
        (output / "trace.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")


def evaluate_workbook(evidence):
    """Summarize available indicators while the scoring policy is unconfirmed."""
    lines = ["# Đối chiếu hồ sơ thị trường", "", "Kính gửi Trưởng phòng Phát triển Kinh doanh", "",
             f"Nguồn — {Path(evidence['source']).name}, sheet `{evidence['sheet']}`.", "",
             "| Địa bàn | Hồ sơ | Khớp WMS hoàn toàn | SLA được ghi nhận khả thi | Mã hồ sơ lặp |",
             "|---|---:|---:|---:|---:|"]
    for area, item in evidence["areas"].items():
        distributions = item["distributions"]
        fit = distributions["Độ Tương Thích Sản Phẩm"].get("Khớp hoàn toàn", 0)
        sla = distributions["Khả Năng Đáp Ứng của Hưng Phát"].get("Khả thi (SLA phù hợp)", 0)
        lines.append(f"| {area} | {item['leads']} | {fit} | {sla} | {item['repeated_record_ids']} |")
    lines += ["", "Các chỉ số là số đếm nhãn trong workbook. Phân bố kỳ, nguồn, cờ trùng và dòng tham chiếu nằm trong comparison.json.",
              "", "## Điểm MCDA ghi trong workbook", "",
              "Điểm và kết luận dưới đây được trích theo ô nguồn. Điểm số hiển thị tối đa ba chữ số thập phân.",
              "", "| Địa bàn | Khớp WMS | Triển khai | Cạnh tranh | Quy mô | Tổng điểm | Kết luận nguồn |",
              "|---|---|---|---|---|---|---|"]
    for area in evidence["areas"]:
        scores = evidence["recorded_mcda"].get(area, {})
        cells = [area]
        for key in ("fit", "deployment", "competition", "scale", "total", "decision"):
            entry = scores.get(key, {})
            value = entry.get("value")
            valid = isinstance(value, str) and value.strip() if key == "decision" else type(value) in (int, float) and math.isfinite(value)
            if not valid:
                cells.append("Cần kiểm tra hoặc bổ sung")
                continue
            display = f"{value:.3f}".rstrip("0").rstrip(".") if isinstance(value, float) else str(value)
            display = display.replace("|", r"\|").replace("\n", " ")
            cells.append(f"{display} (`{entry['cell']}`)")
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
              "", "## Quyết định và điều kiện bổ sung", "",
              "Đề xuất ghi trong workbook — " + (", ".join(evidence["recorded_proposal"])
                                               or "Cần kiểm tra hoặc bổ sung"), "",
              "Cần xác minh căn cứ chấm và điều kiện sàng lọc trước khi duyệt đề xuất.", ""]
    lines += [f"- {condition}." for condition in evidence["required"]]
    lines += ["", "## Kế hoạch khảo sát", ""]
    if not evidence["recorded_proposal"]:
        lines.append("Cần xác minh địa bàn ưu tiên trước khi lập kế hoạch.")
    else:
        lines += ["**Chưa hoàn tất.** Nhóm khách lấy từ sheet dữ liệu nguồn sau khi đối chiếu mã hồ sơ trong sheet kế hoạch. Nội dung xác minh dưới đây là đề xuất cần duyệt.", ""]
        for area in evidence["recorded_proposal"]:
            records = evidence["recorded_survey"].get(area, [])
            groups = sorted({str(row["group"]) for row in records
                             if row["group"] and len(row["source_rows"]) == 1})
            unresolved = sum(not row["group"] or len(row["source_rows"]) != 1 for row in records)
            lines += [f"### {area}", "",
                      "- Nhóm khách — " + (", ".join(groups) or "Cần kiểm tra hoặc bổ sung"),
                      "- Xác minh nhu cầu WMS, yêu cầu hỗ trợ tại chỗ và năng lực đáp ứng thực tế.",
                      "- Người phụ trách — Cần kiểm tra hoặc bổ sung."]
            if not groups:
                candidates = evidence["areas"][area]["retail_groups"]
                if candidates:
                    lines.append("- Nhóm ứng viên từ dữ liệu nguồn, chờ duyệt danh sách tiếp cận — " +
                                 ", ".join(f"{group} ({count} hồ sơ)"
                                           for group, count in candidates.most_common()) + ".")
            if unresolved:
                lines.append(f"- Có {unresolved} hồ sơ khảo sát thiếu nhóm khách hoặc chưa đối chiếu được với một dòng nguồn duy nhất.")
            lines.append("")
    return "\n".join(lines) + "\n"


def run_workbook(path, output):
    from audit_leads_workbook import collect_workbook

    output.mkdir(parents=True, exist_ok=False)
    trace = [{"action": "call", "tool": "collect_workbook", "path": str(path.resolve())}]
    try:
        evidence = collect_workbook(path)
        trace.append({"action": "complete", "tool": "collect_workbook", "sha256": evidence["sha256"],
                      "sheet": evidence["sheet"], "records": sum(a["leads"] for a in evidence["areas"].values())})
        trace.append({"action": "call", "tool": "evaluate_workbook"})
        text = evaluate_workbook(evidence)
        trace.append({"action": "complete", "tool": "evaluate_workbook", "status": evidence["status"]})
        (output / "report.md").write_text(text, encoding="utf-8")
        (output / "comparison.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
        trace.append({"action": "success", "outputs": ["report.md", "comparison.json"],
                      "recorded_proposal": evidence["recorded_proposal"],
                      "survey_status": evidence["survey_status"]})
    except Exception as error:
        trace.append({"action": "failure", "error": str(error)})
        raise
    finally:
        (output / "trace.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("input", "output"):
        parser.add_argument(f"--{option}", type=Path, required=True)
    parser.add_argument("--rules", type=Path)
    args = parser.parse_args()
    if args.input.suffix.lower() == ".xlsx" and args.input.is_file():
        if args.rules:
            parser.error("Excel currently supports evidence review. Use a JSON bundle for configured scoring.")
        run_workbook(args.input, args.output)
    else:
        if not args.rules:
            parser.error("--rules is required for a JSON bundle")
        run(args.input, args.rules, args.output)
