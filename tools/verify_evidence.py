#!/usr/bin/env python3
"""Verify immutable SOCFAI test evidence using only the Python standard library."""

from __future__ import annotations

import csv
import hashlib
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = REPO_ROOT / "evidence" / "2026-08-25"
MANIFEST_PATH = EVIDENCE_ROOT / "FILE_MANIFEST.csv"
SIX_PLACES = Decimal("0.000001")

EXPECTED = {
    "ADD": {
        "run_id": "PACKAGE22_add_100_20260825_134055_850",
        "limit": Decimal("1.000000"),
    },
    "MUL": {
        "run_id": "PACKAGE22_mul_100_20260825_142742_621",
        "limit": Decimal("20.000000"),
    },
}

TRUE_FIELDS = (
    "payload_ok",
    "input_roundtrip_checked",
    "c1_roundtrip_correct",
    "c2_roundtrip_correct",
    "correctness",
    "ciphertext_artifacts_checked",
    "c1_artifact_match",
    "c1_artifact_load_success",
    "c2_artifact_match",
    "c2_artifact_load_success",
    "chain_uses_loaded_inputs",
)

SENSITIVE_PATTERNS = {
    "user_profile_path": re.compile(r"(?i)(?:[A-Z]:\\Users\\|/home/|/Users/)"),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "ipv4": re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[^,;\s]+"
    ),
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_manifest(errors: list[str]) -> list[Path]:
    if not MANIFEST_PATH.is_file():
        fail(f"manifest missing: {MANIFEST_PATH}", errors)
        return []

    rows = read_csv(MANIFEST_PATH)
    if len(rows) != 6:
        fail(f"manifest row count is {len(rows)}, expected 6", errors)

    evidence_files: list[Path] = []
    for row in rows:
        path = REPO_ROOT / Path(row["RelativePath"])
        evidence_files.append(path)
        if not path.is_file():
            fail(f"missing evidence file: {row['RelativePath']}", errors)
            continue

        actual_size = path.stat().st_size
        actual_hash = sha256(path)
        expected_size = int(row["Bytes"])
        expected_hash = row["SHA256"].upper()
        if actual_size != expected_size:
            fail(
                f"size mismatch {row['RelativePath']}: {actual_size} != {expected_size}",
                errors,
            )
        if actual_hash != expected_hash:
            fail(
                f"SHA-256 mismatch {row['RelativePath']}: {actual_hash} != {expected_hash}",
                errors,
            )
        if actual_size == expected_size and actual_hash == expected_hash:
            print(f"[PASS] immutable file: {row['RelativePath']}")

    return evidence_files


def verify_sensitive_text(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="strict")
        for label, pattern in SENSITIVE_PATTERNS.items():
            match = pattern.search(text)
            if match:
                fail(f"sensitive pattern {label} in {path.relative_to(REPO_ROOT)}", errors)
        print(f"[PASS] public-safety text scan: {path.relative_to(REPO_ROOT)}")


def quantize(value: Decimal) -> Decimal:
    return value.quantize(SIX_PLACES, rounding=ROUND_HALF_UP)


def verify_operation(operation: str, errors: list[str]) -> None:
    expected = EXPECTED[operation]
    op_dir = EVIDENCE_ROOT / operation
    summary_path = op_dir / "summary.csv"
    raw_path = op_dir / "raw_iterations.csv"
    summary_rows = read_csv(summary_path)
    raw_rows = read_csv(raw_path)

    if len(summary_rows) != 6:
        fail(f"{operation} summary rows={len(summary_rows)}, expected 6", errors)
    if len(raw_rows) != 100:
        fail(f"{operation} raw rows={len(raw_rows)}, expected 100", errors)

    run_ids = {row["run_id"] for row in raw_rows}
    if run_ids != {expected["run_id"]}:
        fail(f"{operation} raw Run ID mismatch: {sorted(run_ids)}", errors)

    iterations = {int(row["iteration"]) for row in raw_rows}
    if iterations != set(range(1, 101)):
        fail(f"{operation} iteration set is not 1..100", errors)

    distinct_inputs = {row["input_values"] for row in raw_rows}
    if len(distinct_inputs) != 100:
        fail(f"{operation} distinct inputs={len(distinct_inputs)}, expected 100", errors)

    for field in TRUE_FIELDS:
        false_rows = [row["iteration"] for row in raw_rows if row[field].lower() != "true"]
        if false_rows:
            fail(f"{operation} {field} false at iterations {false_rows}", errors)

    if any(row["payload_bits"] != "1024" for row in raw_rows):
        fail(f"{operation} payload_bits contains value other than 1024", errors)
    if any(row["c1_roundtrip_verified_slots"] != "32" for row in raw_rows):
        fail(f"{operation} c1 verified slots contains value other than 32", errors)
    if any(row["c2_roundtrip_verified_slots"] != "32" for row in raw_rows):
        fail(f"{operation} c2 verified slots contains value other than 32", errors)
    if any(row["result_verified_active_slots"] != "32" for row in raw_rows):
        fail(f"{operation} result verified slots contains value other than 32", errors)

    summary_by_step = {row["step"]: row for row in summary_rows}
    for number in range(1, 7):
        step = f"step{number}"
        if step not in summary_by_step:
            fail(f"{operation} summary missing {step}", errors)
            continue

        row = summary_by_step[step]
        values = [Decimal(raw[f"{step}_total_ms"]) for raw in raw_rows]
        ordered = sorted(values)
        p95_index = math.ceil(Decimal("0.95") * len(ordered)) - 1
        calculated = {
            "avg_ms": quantize(sum(values) / Decimal(len(values))),
            "p95_ms": quantize(ordered[p95_index]),
            "min_ms": quantize(ordered[0]),
            "max_ms": quantize(ordered[-1]),
        }

        if row["operation"] != operation:
            fail(f"{operation} {step} operation mismatch: {row['operation']}", errors)
        if row["run_id"] != expected["run_id"]:
            fail(f"{operation} {step} Run ID mismatch: {row['run_id']}", errors)
        if row["samples"] != "100":
            fail(f"{operation} {step} samples={row['samples']}, expected 100", errors)

        for field, actual in calculated.items():
            recorded = Decimal(row[field])
            if recorded != actual:
                fail(
                    f"{operation} {step} {field}: recorded={recorded} calculated={actual}",
                    errors,
                )

        limit = Decimal(row["limit_ms"])
        if limit != expected["limit"]:
            fail(f"{operation} {step} limit={limit}, expected {expected['limit']}", errors)
        expected_result = "PASS" if calculated["avg_ms"] <= limit else "FAIL"
        if row["result"] != expected_result:
            fail(
                f"{operation} {step} result={row['result']}, expected {expected_result}",
                errors,
            )

        if not errors or all(f"{operation} {step}" not in error for error in errors):
            print(
                f"[PASS] {operation} {step}: avg={calculated['avg_ms']} "
                f"p95={calculated['p95_ms']} min={calculated['min_ms']} "
                f"max={calculated['max_ms']} limit={limit} result={expected_result}"
            )

    if not errors or all(operation not in error for error in errors):
        print(f"[PASS] {operation}: 100 rows, 100 distinct inputs, validation flags true")


def main() -> int:
    errors: list[str] = []
    evidence_files = verify_manifest(errors)
    verify_sensitive_text(evidence_files, errors)
    for operation in ("ADD", "MUL"):
        verify_operation(operation, errors)

    if errors:
        print(f"Verification failed with {len(errors)} issue(s).")
        return 1

    print("All immutable evidence, statistics, judgement, validation, and safety checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
