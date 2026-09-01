#!/usr/bin/env python3
"""Create byte-preserving per-iteration views from frozen terminal logs."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-25"
OPERATIONS = {"ADD": "Addition", "MUL": "Multiplication"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def extract_operation(operation: str, label: str) -> list[dict[str, object]]:
    source_relative = Path("evidence") / DATE / operation / "terminal_output.txt"
    source_path = ROOT / source_relative
    source = source_path.read_bytes()
    source_hash = sha256(source)
    pattern = re.compile(
        rb"^=+\r?\nBEGIN "
        + re.escape(label.encode("ascii"))
        + rb" depth6 - ITERATION (?P<iteration>\d{3})/100\r?\n.*?^END "
        + re.escape(label.encode("ascii"))
        + rb" depth6 - ITERATION (?P=iteration)/100\r?\n^-+\r?\n",
        re.MULTILINE | re.DOTALL,
    )
    matches = list(pattern.finditer(source))
    iterations = [int(match.group("iteration")) for match in matches]
    if iterations != list(range(1, 101)):
        raise RuntimeError(
            f"{operation}: expected iterations 1..100, observed {iterations}"
        )

    output_dir = ROOT / "evidence" / DATE / operation / "iteration_views"
    output_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    expected_names = set()
    for match in matches:
        iteration = int(match.group("iteration"))
        name = f"iteration_{iteration:03d}.txt"
        expected_names.add(name)
        block = match.group(0)
        output_path = output_dir / name
        output_path.write_bytes(block)
        records.append(
            {
                "Operation": operation,
                "Iteration": iteration,
                "RelativePath": output_path.relative_to(ROOT).as_posix(),
                "Bytes": len(block),
                "SHA256": sha256(block),
                "SourcePath": source_relative.as_posix(),
                "SourceSHA256": source_hash,
                "SourceByteStart": match.start(),
                "SourceByteEndExclusive": match.end(),
            }
        )

    extras = {
        path.name for path in output_dir.glob("iteration_*.txt")
    } - expected_names
    if extras:
        raise RuntimeError(
            f"{operation}: unexpected iteration view files: {sorted(extras)}"
        )
    return records


def main() -> None:
    records: list[dict[str, object]] = []
    for operation, label in OPERATIONS.items():
        records.extend(extract_operation(operation, label))

    manifest_path = ROOT / "evidence" / DATE / "ITERATION_MANIFEST.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(records[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"Created and verified {len(records)} per-iteration files.")
    print(f"Manifest: {manifest_path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
