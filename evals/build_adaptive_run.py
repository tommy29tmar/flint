from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sigil.eval_common import load_jsonl
from sigil.verification import assess_output, verification_failures


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def index_rows(run_paths: list[Path]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for run_path in run_paths:
        for row in load_jsonl(run_path):
            task_id = str(row["task_id"])
            if task_id in indexed:
                raise SystemExit(f"Duplicate task_id '{task_id}' across supplied run files.")
            indexed[task_id] = row
    return indexed


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, int] = {}
    for row in rows:
        variant = str(row["variant"])
        summary[variant] = summary.get(variant, 0) + 1
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an adaptive SIGIL run using verifier-gated fallback selection.")
    parser.add_argument("tasks", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--primary-run", dest="primary_runs", action="append", type=Path, required=True)
    parser.add_argument("--fallback-run", dest="fallback_runs", action="append", type=Path, required=True)
    parser.add_argument("--baseline-run", type=Path, default=None)
    parser.add_argument("--baseline-variant", default="baseline-terse")
    parser.add_argument("--variant-name", default="sigil-adaptive")
    parser.add_argument("--min-must-include", type=float, default=0.75)
    parser.add_argument("--min-exact-literal", type=float, default=0.75)
    parser.add_argument("--allow-repair", action="store_true")
    parser.add_argument("--no-require-parse", action="store_true")
    parser.add_argument("--no-require-mode-match", action="store_true")
    args = parser.parse_args(argv)

    tasks = {str(row["id"]): row for row in load_jsonl(args.tasks)}
    primary_rows = index_rows(args.primary_runs)
    fallback_rows = index_rows(args.fallback_runs)
    baseline_rows: dict[str, dict[str, Any]] = {}
    if args.baseline_run is not None:
        for row in load_jsonl(args.baseline_run):
            if str(row["variant"]) != args.baseline_variant:
                continue
            baseline_rows[str(row["task_id"])] = row

    output_rows: list[dict[str, Any]] = []
    selected_primary = 0
    selected_fallback = 0
    fallback_reasons: dict[str, int] = {}

    if baseline_rows:
        for task_id in tasks:
            matched = baseline_rows.get(task_id)
            if matched is None:
                raise SystemExit(f"Missing baseline row for task '{task_id}' and variant '{args.baseline_variant}'.")
            output_rows.append(matched)

    for task_id, task in tasks.items():
        primary_row = primary_rows.get(task_id)
        fallback_row = fallback_rows.get(task_id)
        if primary_row is None:
            raise SystemExit(f"Missing primary row for task '{task_id}'.")
        if fallback_row is None:
            raise SystemExit(f"Missing fallback row for task '{task_id}'.")

        metrics = assess_output(task, primary_row, root=ROOT)
        failures = verification_failures(
            metrics,
            min_must_include=args.min_must_include,
            min_exact_literal=args.min_exact_literal,
            require_parse=not args.no_require_parse,
            require_mode_match=not args.no_require_mode_match,
            allow_repair=args.allow_repair,
        )
        if failures:
            chosen = dict(fallback_row)
            selected_fallback += 1
            for reason in failures:
                fallback_reasons[reason] = fallback_reasons.get(reason, 0) + 1
            chosen["adaptive_selected_from"] = "fallback"
            chosen["adaptive_rejection"] = failures
        else:
            chosen = dict(primary_row)
            selected_primary += 1
            chosen["adaptive_selected_from"] = "primary"

        chosen["variant"] = args.variant_name
        chosen["adaptive_primary_variant"] = primary_row["variant"]
        chosen["adaptive_fallback_variant"] = fallback_row["variant"]
        chosen["adaptive_verifier"] = metrics
        output_rows.append(chosen)

    append_jsonl(args.out, output_rows)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "count": len(output_rows),
                "selected_primary": selected_primary,
                "selected_fallback": selected_fallback,
                "fallback_reasons": fallback_reasons,
                "variants": summarize_rows(output_rows),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
