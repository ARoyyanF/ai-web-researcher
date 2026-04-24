#!/usr/bin/env python3
"""Extract YouTube transcripts from a URL list using yt-dlp."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from typing import Iterable, NamedTuple


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_LINKS_FILE = ROOT_DIR / "raw" / "youtube-url.txt"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "raw" / "transcripts"
DEFAULT_CLEAN_OUTPUT_DIR = ROOT_DIR / "artifacts" / "transcripts_clean"
URL_HEADERS = ("url", "link", "video_url", "youtube_url", "href")
TIMESTAMP_PATTERN = re.compile(
    r"(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}),(?P<millis>\d{3})"
)
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class Caption(NamedTuple):
    start_seconds: float
    text: str


def sanitize_filename(name: str, replacement: str = "_") -> str:
    sanitized = INVALID_FILENAME_CHARS.sub(replacement, name)
    sanitized = re.sub(r"\s+", " ", sanitized).strip(" .")
    return sanitized or "untitled"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download SRT transcripts for videos listed in a URL file."
    )
    parser.add_argument(
        "links_file",
        nargs="?",
        type=Path,
        default=DEFAULT_LINKS_FILE,
        help=f"Text or CSV file containing video URLs. Defaults to {DEFAULT_LINKS_FILE}",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for downloaded .srt files. Defaults to {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--clean-output-dir",
        type=Path,
        default=DEFAULT_CLEAN_OUTPUT_DIR,
        help=f"Directory for cleaned Markdown transcripts. Defaults to {DEFAULT_CLEAN_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--timestamp-window",
        type=int,
        default=30,
        help="Seconds to merge captions under one timestamp in cleaned Markdown. Defaults to 30.",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Subtitle language code passed to yt-dlp. Defaults to en",
    )
    parser.add_argument(
        "--manual-subs-only",
        action="store_true",
        help="Download only manually provided subtitles, not auto-generated subtitles.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Keep processing remaining links when yt-dlp fails for a URL.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=20,
        help="Number of parallel yt-dlp jobs. Defaults to 20.",
    )
    return parser.parse_args()


def normalize_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def looks_like_url(value: str) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def iter_links_from_text(path: Path) -> Iterable[str]:
    with path.open("r", encoding="utf-8-sig") as text_file:
        for raw_line in text_file:
            link = raw_line.strip()
            if link and not link.startswith("#"):
                yield link


def iter_links_from_csv(path: Path) -> Iterable[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        sample = csv_file.read(4096)
        csv_file.seek(0)

        has_header = csv.Sniffer().has_header(sample) if sample.strip() else False
        if has_header:
            reader = csv.DictReader(csv_file)
            fieldnames = [field.strip() for field in (reader.fieldnames or []) if field]
            url_field = next(
                (field for field in fieldnames if field.lower() in URL_HEADERS),
                fieldnames[0] if fieldnames else None,
            )
            if not url_field:
                return

            for row in reader:
                link = (row.get(url_field) or "").strip()
                if looks_like_url(link):
                    yield link
            return

        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                continue
            link = row[0].strip()
            if looks_like_url(link):
                yield link


def iter_links(path: Path) -> Iterable[str]:
    if path.suffix.lower() == ".csv":
        yield from iter_links_from_csv(path)
        return

    yield from iter_links_from_text(path)


def build_yt_dlp_command(
    url: str,
    output_dir: Path,
    lang: str,
    manual_subs_only: bool,
) -> list[str]:
    output_template = str(output_dir / "%(title)s.%(ext)s")
    command = [
        "yt-dlp",
        "--skip-download",
        "--windows-filenames",
        "--sub-lang",
        lang,
        "--sub-format",
        "srt/best",
        "--convert-subs",
        "srt",
        "-o",
        output_template,
    ]

    command.append("--write-subs" if manual_subs_only else "--write-auto-subs")
    command.append(url)
    return command


def parse_srt_timestamp(timestamp: str) -> float:
    match = TIMESTAMP_PATTERN.search(timestamp)
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {timestamp}")

    hours = int(match.group("hours"))
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis = int(match.group("millis"))
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def format_markdown_timestamp(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def clean_caption_text(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_srt(srt_path: Path) -> list[Caption]:
    content = srt_path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = re.split(r"\r?\n\s*\r?\n", content.strip())
    captions: list[Caption] = []

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        timestamp_index = next(
            (index for index, line in enumerate(lines) if "-->" in line),
            None,
        )
        if timestamp_index is None:
            continue

        start_timestamp = lines[timestamp_index].split("-->", 1)[0].strip()
        text = clean_caption_text(lines[timestamp_index + 1 :])
        if text:
            captions.append(
                Caption(
                    start_seconds=parse_srt_timestamp(start_timestamp),
                    text=text,
                )
            )

    return captions


def write_clean_markdown(
    srt_path: Path,
    clean_output_dir: Path,
    timestamp_window: int,
) -> Path | None:
    captions = parse_srt(srt_path)
    if not captions:
        return None

    timestamp_window = max(1, timestamp_window)
    title = srt_path.stem
    language_suffix = srt_path.suffixes[-2] if len(srt_path.suffixes) > 1 else ""
    if language_suffix:
        title = title.removesuffix(language_suffix)
    title = sanitize_filename(title)
    markdown_path = clean_output_dir / f"{title}.md"

    lines = [f"# {title}", ""]
    group_start = captions[0].start_seconds
    group_text: list[str] = []

    def flush_group() -> None:
        if group_text:
            timestamp = format_markdown_timestamp(group_start)
            lines.append(f"[{timestamp}] {' '.join(group_text)}")
            lines.append("")

    for caption in captions:
        if caption.start_seconds - group_start >= timestamp_window:
            flush_group()
            group_start = caption.start_seconds
            group_text = [caption.text]
        else:
            group_text.append(caption.text)

    flush_group()
    clean_output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return markdown_path


def clean_srt_directory(
    srt_dir: Path,
    clean_output_dir: Path,
    timestamp_window: int,
) -> tuple[list[Path], list[tuple[Path, str]]]:
    markdown_files: list[Path] = []
    failures: list[tuple[Path, str]] = []

    for srt_path in sorted(srt_dir.glob("*.srt")):
        try:
            markdown_path = write_clean_markdown(
                srt_path=srt_path,
                clean_output_dir=clean_output_dir,
                timestamp_window=timestamp_window,
            )
            if markdown_path:
                markdown_files.append(markdown_path)
            else:
                failures.append((srt_path, "No captions found"))
        except Exception as exc:
            failures.append((srt_path, str(exc)))

    return markdown_files, failures


def run_yt_dlp_job(
    index: int,
    total: int,
    url: str,
    output_dir: Path,
    lang: str,
    manual_subs_only: bool,
) -> tuple[int, str, int]:
    print(f"[{index}/{total}] Extracting transcript: {url}")
    command = build_yt_dlp_command(
        url=url,
        output_dir=output_dir,
        lang=lang,
        manual_subs_only=manual_subs_only,
    )
    result = subprocess.run(command, check=False)
    return index, url, result.returncode


def print_recap(
    links_file: Path,
    output_dir: Path,
    clean_output_dir: Path,
    total: int,
    workers: int,
    lang: str,
    timestamp_window: int,
    manual_subs_only: bool,
    successes: list[tuple[int, str]],
    failures: list[tuple[int, str, int]],
    cancelled: int,
    markdown_files: list[Path],
    markdown_failures: list[tuple[Path, str]],
) -> None:
    subtitle_source = "manual subtitles only" if manual_subs_only else "auto-generated subtitles"
    print("")
    print("Job recap")
    print("---------")
    print(f"Input URL file: {links_file}")
    print(f"SRT output directory: {output_dir}")
    print(f"Clean Markdown output directory: {clean_output_dir}")
    print(f"Subtitle language: {lang}")
    print(f"Subtitle source: {subtitle_source}")
    print("Subtitle format fallback: srt/best, then convert to srt")
    print(f"Clean Markdown timestamp window: {timestamp_window} seconds")
    print(f"Parallel workers: {workers}")
    print(f"Total URLs queued: {total}")
    print(f"Successful extractions: {len(successes)}")
    print(f"Failed extractions: {len(failures)}")
    print(f"Clean Markdown files written: {len(markdown_files)}")
    print(f"Clean Markdown failures: {len(markdown_failures)}")
    if cancelled:
        print(f"Cancelled or skipped after failure: {cancelled}")

    if successes:
        print("")
        print("Successful URLs:")
        for index, url in sorted(successes):
            print(f"  [{index}/{total}] {url}")

    if failures:
        print("")
        print("Failures:")
        for index, url, returncode in sorted(failures):
            print(f"  [{index}/{total}] return code {returncode}: {url}")

    if markdown_failures:
        print("")
        print("Clean Markdown failures:")
        for srt_path, reason in markdown_failures:
            print(f"  {srt_path.name}: {reason}")


def extract_transcripts(args: argparse.Namespace) -> int:
    if not shutil.which("yt-dlp"):
        print("Error: yt-dlp is not installed or is not on PATH.", file=sys.stderr)
        return 1

    links_file = normalize_path(args.links_file)
    output_dir = normalize_path(args.output_dir)
    clean_output_dir = normalize_path(args.clean_output_dir)

    if not links_file.exists():
        print(f"Error: links file not found: {links_file}", file=sys.stderr)
        return 1

    links = list(iter_links(links_file))
    if not links:
        print(f"No links found in {links_file}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    clean_output_dir.mkdir(parents=True, exist_ok=True)

    max_workers = max(1, args.workers)
    successes: list[tuple[int, str]] = []
    failures: list[tuple[int, str, int]] = []
    markdown_files: list[Path] = []
    markdown_failures: list[tuple[Path, str]] = []
    cancelled = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                run_yt_dlp_job,
                index,
                len(links),
                url,
                output_dir,
                args.lang,
                args.manual_subs_only,
            )
            for index, url in enumerate(links, start=1)
        ]

        for future in as_completed(futures):
            index, url, returncode = future.result()
            if returncode != 0:
                failures.append((index, url, returncode))
                print(f"Failed to extract transcript: {url}", file=sys.stderr)
                if not args.continue_on_error:
                    for pending_future in futures:
                        if pending_future.cancel():
                            cancelled += 1
                    print_recap(
                        links_file=links_file,
                        output_dir=output_dir,
                        clean_output_dir=clean_output_dir,
                        total=len(links),
                        workers=max_workers,
                        lang=args.lang,
                        timestamp_window=args.timestamp_window,
                        manual_subs_only=args.manual_subs_only,
                        successes=successes,
                        failures=failures,
                        cancelled=cancelled,
                        markdown_files=markdown_files,
                        markdown_failures=markdown_failures,
                    )
                    return returncode
            else:
                successes.append((index, url))

    markdown_files, markdown_failures = clean_srt_directory(
        srt_dir=output_dir,
        clean_output_dir=clean_output_dir,
        timestamp_window=args.timestamp_window,
    )

    if failures:
        print_recap(
            links_file=links_file,
            output_dir=output_dir,
            clean_output_dir=clean_output_dir,
            total=len(links),
            workers=max_workers,
            lang=args.lang,
            timestamp_window=args.timestamp_window,
            manual_subs_only=args.manual_subs_only,
            successes=successes,
            failures=failures,
            cancelled=cancelled,
            markdown_files=markdown_files,
            markdown_failures=markdown_failures,
        )
        print(f"Completed with {len(failures)} failed URL(s).", file=sys.stderr)
        return 1

    print_recap(
        links_file=links_file,
        output_dir=output_dir,
        clean_output_dir=clean_output_dir,
        total=len(links),
        workers=max_workers,
        lang=args.lang,
        timestamp_window=args.timestamp_window,
        manual_subs_only=args.manual_subs_only,
        successes=successes,
        failures=failures,
        cancelled=cancelled,
        markdown_files=markdown_files,
        markdown_failures=markdown_failures,
    )
    print(f"Transcripts written to {output_dir}")
    print(f"Clean Markdown transcripts written to {clean_output_dir}")
    return 0


def main() -> None:
    raise SystemExit(extract_transcripts(parse_args()))


if __name__ == "__main__":
    main()
