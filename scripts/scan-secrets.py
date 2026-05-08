#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


DENY_FILE_NAMES = {
    ".env",
    "auth.json",
    "auth-profiles.json",
    "sessions.json",
}

DENY_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "cognee",
    "logs",
    "tmp",
}

SECRET_PATTERNS = [
    re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bpplx-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b[A-Za-z0-9]{4,}\|[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*(?!replace_|your_|example|<|\\$\\{|\\$)[\"']?[A-Za-z0-9_./|:-]{12,}"),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        rel_parts = set(path.relative_to(root).parts)
        if rel_parts & DENY_DIR_NAMES:
            continue
        if path.is_file():
            yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []

    for path in iter_files(root):
        if path.name in DENY_FILE_NAMES:
            findings.append(f"forbidden file name: {path.relative_to(root)}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                findings.append(f"possible secret: {path.relative_to(root)}:{line_no}")

    if findings:
        print("Secret scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Secret scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
