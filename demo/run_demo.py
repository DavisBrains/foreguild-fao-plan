#!/usr/bin/env python3
"""Foreguild demo: T0 acceptance harness + FIP→mandate compile/enforce.

No chain, no wallet. Pure local files. From the repo:
  cd demo && python3 run_demo.py
"""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_json(p: Path):
    return json.loads(p.read_text())

def check_file_exists(workspace: Path, path: str):
    ok = (workspace / path).is_file()
    return ok, f"file_exists {path}: {'PASS' if ok else 'FAIL'}"

def check_csv_no_blank(workspace: Path, path: str, column: str):
    fp = workspace / path
    if not fp.is_file():
        return False, f"csv_no_blank_amount {path}: FAIL (missing file)"
    with fp.open(newline="") as f:
        rows = list(csv.DictReader(f))
    blanks = [i for i, r in enumerate(rows, start=2) if not str(r.get(column, "")).strip()]
    ok = len(blanks) == 0
    detail = "none" if ok else f"blank rows {blanks}"
    return ok, f"csv_no_blank_amount {path}.{column}: {'PASS' if ok else 'FAIL'} ({detail})"

def check_row_count_min(workspace: Path, path: str, min_rows: int):
    fp = workspace / path
    if not fp.is_file():
        return False, f"row_count_min {path}: FAIL (missing file)"
    with fp.open(newline="") as f:
        n = sum(1 for _ in csv.DictReader(f))
    ok = n >= min_rows
    return ok, f"row_count_min {path}>={min_rows}: {'PASS' if ok else 'FAIL'} (got {n})"

HANDLERS = {
    "file_exists": lambda ws, t: check_file_exists(ws, t["path"]),
    "csv_no_blank_amount": lambda ws, t: check_csv_no_blank(ws, t["path"], t["column"]),
    "row_count_min": lambda ws, t: check_row_count_min(ws, t["path"], t["min_rows"]),
}

def run_harness(task: dict, workspace: Path):
    print(f"\n=== T0 harness for {task['task_id']}: {task['title']} ===")
    try:
        rel = workspace.resolve().relative_to(ROOT)
    except ValueError:
        rel = workspace
    print(f"workspace: {rel.as_posix()}")
    results = []
    for t in task["acceptance_tests"]:
        fn = HANDLERS[t["type"]]
        ok, msg = fn(workspace, t)
        results.append(ok)
        print(("  ✓ " if ok else "  ✗ ") + msg)
    verdict = "ACCEPT" if all(results) else "REJECT"
    print(f"VERDICT: {verdict}")
    return verdict == "ACCEPT"

def compile_mandate(fip_path: Path, out_path: Path):
    fip = load_json(fip_path)
    assert fip["status"] == "passed", "refuse to compile non-passed FIP"
    mandate = {
        "source_fip": fip["fip_id"],
        "market_id": fip["market_id"],
        "compiled_at": fip["compiled_at"],
        **fip["mandate"],
    }
    out_path.write_text(json.dumps(mandate, indent=2) + "\n")
    print(f"\n=== Compiled mandate from {fip['fip_id']} → {out_path.name} ===")
    print(json.dumps(mandate, indent=2))
    return mandate

def try_action(mandate: dict, action: dict):
    print(f"\n=== Mandate check: {action['name']} ===")
    reasons = []
    if action.get("category") not in mandate["allowed_categories"]:
        reasons.append(f"category '{action.get('category')}' not in {mandate['allowed_categories']}")
    if action.get("ticket_usdc", 0) > mandate["max_ticket_usdc"]:
        reasons.append(f"ticket {action['ticket_usdc']} > max_ticket {mandate['max_ticket_usdc']}")
    if action.get("worker_spend_today_usdc", 0) + action.get("ticket_usdc", 0) > mandate["worker_daily_spend_cap_usdc"]:
        reasons.append(
            f"spend {action.get('worker_spend_today_usdc',0)}+{action.get('ticket_usdc',0)} "
            f"> daily cap {mandate['worker_daily_spend_cap_usdc']}"
        )
    if reasons:
        print("BLOCKED:")
        for r in reasons:
            print("  -", r)
        return False
    print("ALLOWED")
    return True

def main():
    task = load_json(ROOT / "sample_task" / "task.json")
    print("Foreguild local demo (no chain, no wallet)")
    print("1) Bad submission (blank amount left in place)")
    run_harness(task, ROOT / "fixtures" / "bad")
    print("\n2) Good submission (blanks normalized to 0.00)")
    run_harness(task, ROOT / "fixtures" / "good")
    mandate = compile_mandate(
        ROOT / "mandates" / "fip-03-passed.json",
        ROOT / "mandates" / "active_mandate.json",
    )
    try_action(mandate, {
        "name": "in-mandate csv-cleanup job ($70)",
        "category": "csv-cleanup",
        "ticket_usdc": 70,
        "worker_spend_today_usdc": 40,
    })
    try_action(mandate, {
        "name": "OUT-OF-MANDATE marketing-copy job ($70)",
        "category": "marketing-copy",
        "ticket_usdc": 70,
        "worker_spend_today_usdc": 40,
    })
    try_action(mandate, {
        "name": "over daily spend cap",
        "category": "csv-cleanup",
        "ticket_usdc": 70,
        "worker_spend_today_usdc": 180,
    })
    print("\nDemo complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
