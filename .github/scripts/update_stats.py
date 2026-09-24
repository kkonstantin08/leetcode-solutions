#!/usr/bin/env python3
"""Update the automatically generated LeetCode statistics in README.md."""

from __future__ import annotations

import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START_MARKER = "<!-- LEETCODE_STATS_START -->"
END_MARKER = "<!-- LEETCODE_STATS_END -->"

PROBLEM_DIRECTORY = re.compile(r"^\d{4,}-")
DIFFICULTY_BADGE = re.compile(r"Difficulty-(Easy|Medium|Hard)-", re.IGNORECASE)

LANGUAGE_BY_SUFFIX = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".kt": "Kotlin",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
}


def latest_commit_date() -> str:
    result = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--format=%cI",
            "--",
            ":(glob)[0-9]*/*",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    raw_date = result.stdout.strip()
    if not raw_date:
        return "Not yet"

    try:
        date = datetime.fromisoformat(raw_date).astimezone(timezone.utc)
    except ValueError:
        return raw_date
    return date.strftime("%Y-%m-%d %H:%M UTC")


def collect_stats() -> tuple[int, Counter[str], Counter[str]]:
    problem_directories = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and PROBLEM_DIRECTORY.match(path.name)
    )

    difficulties: Counter[str] = Counter()
    languages: Counter[str] = Counter()

    for problem_directory in problem_directories:
        readme = problem_directory / "README.md"
        if readme.is_file():
            match = DIFFICULTY_BADGE.search(readme.read_text(encoding="utf-8"))
            if match:
                difficulties[match.group(1).title()] += 1

        for solution in problem_directory.iterdir():
            if not solution.is_file():
                continue
            language = LANGUAGE_BY_SUFFIX.get(solution.suffix.lower())
            if language:
                languages[language] += 1

    return len(problem_directories), languages, difficulties


def build_stats(total: int, languages: Counter[str], difficulties: Counter[str]) -> str:
    last_synced = latest_commit_date()

    rows = [
        "| Metric | Value |",
        "|---|---:|",
        f"| Problems solved | **{total}** |",
        f"| Languages | **{len(languages)}** |",
        f"| Last synced | {last_synced} |",
    ]

    for difficulty in ("Easy", "Medium", "Hard"):
        rows.append(f"| {difficulty} | {difficulties[difficulty]} |")

    return f"{START_MARKER}\n" + "\n".join(rows) + f"\n{END_MARKER}"


def replace_stats(readme: str, generated: str) -> str:
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )
    updated, count = pattern.subn(generated, readme, count=1)
    if count != 1:
        raise RuntimeError(
            f"Expected one stats block in {README}, found {count}. "
            f"Both {START_MARKER} and {END_MARKER} are required."
        )
    return updated


def main() -> None:
    total, languages, difficulties = collect_stats()
    generated = build_stats(total, languages, difficulties)
    original = README.read_text(encoding="utf-8")
    updated = replace_stats(original, generated)

    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print(f"Updated README: {total} problems, {len(languages)} languages.")
    else:
        print("README statistics are already up to date.")


if __name__ == "__main__":
    main()
