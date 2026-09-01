# Per-iteration terminal log views

This directory contains derived, byte-preserving slices of the immutable ADD and
MUL `terminal_output.txt` files.

- `ADD/iteration_001.txt` through `ADD/iteration_100.txt`
- `MUL/iteration_001.txt` through `MUL/iteration_100.txt`
- `ITERATION_MANIFEST.csv`: source identity, byte offsets, sizes, and SHA-256 hashes

Each TXT file contains one complete `BEGIN ... ITERATION n/100` through
`END ... ITERATION n/100` block, including its surrounding separator lines.
These files are navigation aids, not independent executions or additional
measurements. The immutable evidence remains under `evidence/2026-08-25/`.

Regenerate the views from the repository root with:

```text
python tools/split_iterations.py
```

This command rewrites only the files under `derived/2026-08-25/`. It does not
modify the immutable source files under `evidence/2026-08-25/`. After
regeneration, run `python tools/verify_evidence.py` from the repository root.
