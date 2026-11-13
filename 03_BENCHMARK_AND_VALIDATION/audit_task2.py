"""Generate synthetic fixtures and audit the public CLI without touching input files."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "02_CORE_PIPELINE_ENGINES" / "task2_market_agent.py"
AREAS = ["A", "B", "C", "D"]
KINDS = ["market", "competitor", "feedback", "product", "capacity"]


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def fixture(folder, case):
    folder.mkdir()
    rows = []
    scores = [4, 3, 2, 1] if case != "new_input" else [1, 2, 3, 4]
    for area, score, hours in zip(AREAS, scores, [1, 2, 2.01, 1.99]):
        for kind in KINDS:
            metrics = {}
            if kind == "market":
                metrics = {f"criterion_{index}": {"value": int(index <= score), "unit": "flag"}
                           for index in range(1, 5)}
                if case == "missing" and area == "D":
                    del metrics["criterion_1"]
            if kind == "capacity":
                metrics = {"hours": {"value": hours, "unit": "h"}}
            rows.append({"area": area, "kind": kind, "source": f"SYNTHETIC-{area}-{kind}",
                         "period": "fixture", "locator": "row 1", "metrics": metrics})
    if case == "conflict":
        rows.append({**rows[0], "source": "SYNTHETIC-CONFLICT",
                     "metrics": {"criterion_1": {"value": 0, "unit": "flag"}}})
    rows.append(rows[0])
    write(folder / "manifest.json", {"areas": AREAS, "documents": ["facts.json"]})
    write(folder / "facts.json", rows)


def audit(output):
    output.mkdir(parents=True)
    rules = output / "synthetic_rules.json"
    metrics = {f"criterion_{index}": {"operator": ">=", "threshold": 1, "weight": 1,
               "unit": "flag", "period": "fixture", "kinds": ["market"]} for index in range(1, 5)}
    metrics["hours"] = {"operator": "<=", "threshold": 2, "weight": 1, "unit": "h",
                        "period": "fixture", "kinds": ["capacity"], "gate": True}
    survey = {area: {"group": "Synthetic retail chains", "verify": "On-site response time",
                     "owner": "Deployment team"} for area in AREAS}
    write(rules, {"version": "synthetic-only", "metrics": metrics, "survey": survey})
    summary = {}
    for case, expected in {"normal": ["A", "B"], "missing": [], "boundary": ["A", "B"],
                           "conflict": [], "new_input": ["D", "B"]}.items():
        inputs, results = output / f"{case}_input", output / case
        fixture(inputs, case)
        before = {p.name: p.read_bytes() for p in inputs.iterdir()}
        subprocess.run([sys.executable, str(ENGINE), "--input", str(inputs), "--rules", str(rules),
                        "--output", str(results)], check=True)
        actual = json.loads((results / "comparison.json").read_text(encoding="utf-8"))
        trace = json.loads((results / "trace.json").read_text(encoding="utf-8"))
        assert actual["selected"] == expected, (case, actual["selected"])
        assert [row["area"] for row in actual["areas"]] == AREAS
        assert [event["tool"] for event in trace if event["action"] == "call"] == ["collect", "evaluate"]
        assert any(event["action"] == "duplicate" for event in trace)
        assert before == {p.name: p.read_bytes() for p in inputs.iterdir()}
        assert (results / "report.md").is_file()
        if case == "boundary":
            assert [row["checks"][-1]["status"] for row in actual["areas"]] == ["pass", "pass", "fail", "pass"]
        if case in {"missing", "conflict"}:
            assert any(check["status"] == case for row in actual["areas"] for check in row["checks"])
        summary[case] = {"expected": expected, "actual": actual["selected"], "status": "pass"}
    write(output / "audit.json", summary)
    print(f"PASS {len(summary)} synthetic CLI audit cases: {output / 'audit.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    audit(parser.parse_args().output)
