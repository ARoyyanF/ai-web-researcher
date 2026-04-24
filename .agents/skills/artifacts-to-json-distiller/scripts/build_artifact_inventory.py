#!/usr/bin/env python3
"""Build a compact inventory JSON for files under an artifacts root."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import UTC, datetime
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".txt", ".json", ".csv"}
TIMESTAMP_RE = re.compile(r"\[(\d{2}:\d{2}(?::\d{2})?)\]")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
WHITESPACE_RE = re.compile(r"\s+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an inventory JSON for files under an artifacts directory."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("artifacts"),
        help="Root directory to scan. Defaults to artifacts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/digests/artifact_inventory.json"),
        help="Output JSON path. Defaults to artifacts/digests/artifact_inventory.json",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=280,
        help="Maximum preview length per file. Defaults to 280",
    )
    parser.add_argument(
        "--max-headings",
        type=int,
        default=5,
        help="Maximum headings captured per file. Defaults to 5",
    )
    parser.add_argument(
        "--max-anchors",
        type=int,
        default=5,
        help="Maximum anchors captured per file. Defaults to 5",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"Could not decode {path}")


def collect_headings(text: str, limit: int) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            headings.append(normalize_text(match.group(1)))
            if len(headings) >= limit:
                break
    return headings


def collect_anchors(text: str, limit: int) -> list[str]:
    anchors: list[str] = []
    for match in TIMESTAMP_RE.finditer(text):
        anchor = match.group(1)
        if anchor not in anchors:
            anchors.append(anchor)
        if len(anchors) >= limit:
            break
    return anchors


def summarize_markdown_or_text(text: str, preview_chars: int) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    preview = normalize_text(" ".join(lines[:3]))
    return preview[:preview_chars].rstrip()


def summarize_json(text: str, preview_chars: int) -> tuple[str, list[str]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if isinstance(data, dict):
        keys = list(data.keys())[:8]
        summary = f"JSON object with keys: {', '.join(keys)}"
        return summary[:preview_chars].rstrip(), keys
    if isinstance(data, list):
        summary = f"JSON array with {len(data)} item(s)"
        return summary[:preview_chars].rstrip(), []
    return f"JSON scalar value of type {type(data).__name__}"[:preview_chars].rstrip(), []


def summarize_csv(path: Path, preview_chars: int) -> tuple[str, list[str], int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)

    row_count = len(rows)
    header = rows[0] if rows else []
    header_preview = ", ".join(cell.strip() for cell in header[:8] if cell.strip())
    if header_preview:
        summary = f"CSV with {row_count} row(s); header: {header_preview}"
    else:
        summary = f"CSV with {row_count} row(s)"
    return summary[:preview_chars].rstrip(), header, row_count


def build_entry(
    path: Path,
    root: Path,
    preview_chars: int,
    max_headings: int,
    max_anchors: int,
) -> dict:
    rel_path = path.relative_to(root.parent).as_posix()
    suffix = path.suffix.lower()
    entry = {
        "path": rel_path,
        "type": suffix.lstrip("."),
        "size_bytes": path.stat().st_size,
        "status": "included",
        "summary": "",
        "anchors": [],
        "headings": [],
    }

    if suffix not in SUPPORTED_SUFFIXES:
        entry["status"] = "skipped_unsupported"
        entry["summary"] = f"Unsupported file type: {suffix or 'no extension'}"
        return entry

    try:
        if suffix == ".csv":
            summary, header, row_count = summarize_csv(path, preview_chars)
            entry["summary"] = summary
            entry["csv_header"] = header[:12]
            entry["row_count"] = row_count
            return entry

        text = read_text(path)
        entry["anchors"] = collect_anchors(text, max_anchors)

        if suffix in {".md", ".txt"}:
            entry["headings"] = collect_headings(text, max_headings)
            entry["summary"] = summarize_markdown_or_text(text, preview_chars)
            entry["char_count"] = len(text)
            entry["line_count"] = len(text.splitlines())
            return entry

        if suffix == ".json":
            summary, keys = summarize_json(text, preview_chars)
            entry["summary"] = summary
            entry["json_keys"] = keys
            entry["char_count"] = len(text)
            return entry
    except Exception as exc:  # noqa: BLE001
        entry["status"] = "skipped_unreadable"
        entry["summary"] = str(exc)

    return entry


def discover_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()

    if not root.exists():
        raise SystemExit(f"Input root does not exist: {root}")

    files = discover_files(root)
    entries = [
        build_entry(
            path=path,
            root=root,
            preview_chars=max(80, args.preview_chars),
            max_headings=max(1, args.max_headings),
            max_anchors=max(1, args.max_anchors),
        )
        for path in files
    ]

    status_counts = {
        "included": sum(1 for entry in entries if entry["status"] == "included"),
        "skipped_unsupported": sum(
            1 for entry in entries if entry["status"] == "skipped_unsupported"
        ),
        "skipped_unreadable": sum(
            1 for entry in entries if entry["status"] == "skipped_unreadable"
        ),
    }

    payload = {
        "meta": {
            "schema_version": "1.0",
            "generated_at": datetime.now(UTC).isoformat(),
            "input_root": root.as_posix(),
            "output_path": output.as_posix(),
            "included_file_count": status_counts["included"],
            "skipped_file_count": status_counts["skipped_unsupported"]
            + status_counts["skipped_unreadable"],
            "status_counts": status_counts,
        },
        "source_inventory": entries,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote artifact inventory to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
