#!/usr/bin/env python3
"""Categorize source URLs into typed output files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_FILE = ROOT_DIR / "sources.txt"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "raw"


@dataclass(frozen=True)
class UrlCategory:
    name: str
    output_name: str
    domains: tuple[str, ...]

    def matches(self, url: str) -> bool:
        hostname = urlparse(url).netloc.lower()
        if not hostname:
            return False
        return any(
            hostname == domain or hostname.endswith(f".{domain}")
            for domain in self.domains
        )


CATEGORIES: tuple[UrlCategory, ...] = (
    UrlCategory(
        name="youtube",
        output_name="youtube-url.txt",
        domains=("youtube.com", "youtu.be", "m.youtube.com"),
    ),
)
FALLBACK_CATEGORY = UrlCategory(
    name="other",
    output_name="other-url.txt",
    domains=(),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Categorize URLs from a source list into per-type files."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help=f"Input file containing one URL per line. Defaults to {DEFAULT_INPUT_FILE}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for categorized URL files. Defaults to {DEFAULT_OUTPUT_DIR}",
    )
    return parser.parse_args()


def normalize_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def iter_urls(input_file: Path) -> list[str]:
    urls: list[str] = []
    for raw_line in input_file.read_text(encoding="utf-8-sig").splitlines():
        url = raw_line.strip()
        if url and not url.startswith("#"):
            urls.append(url)
    return urls


def resolve_category(url: str) -> UrlCategory:
    for category in CATEGORIES:
        if category.matches(url):
            return category
    return FALLBACK_CATEGORY


def write_output(path: Path, urls: list[str]) -> None:
    content = "\n".join(urls)
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")


def categorize_sources(args: argparse.Namespace) -> int:
    input_file = normalize_path(args.input_file)
    output_dir = normalize_path(args.output_dir)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output_dir.mkdir(parents=True, exist_ok=True)
    urls = iter_urls(input_file)

    grouped_urls: dict[str, list[str]] = {
        category.name: [] for category in (*CATEGORIES, FALLBACK_CATEGORY)
    }
    for url in urls:
        category = resolve_category(url)
        grouped_urls[category.name].append(url)

    for category in (*CATEGORIES, FALLBACK_CATEGORY):
        output_path = output_dir / category.output_name
        write_output(output_path, grouped_urls[category.name])
        print(f"{category.name}: {len(grouped_urls[category.name])} -> {output_path}")

    return 0


def main() -> None:
    raise SystemExit(categorize_sources(parse_args()))


if __name__ == "__main__":
    main()
