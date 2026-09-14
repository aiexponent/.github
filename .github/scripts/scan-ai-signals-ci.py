#!/usr/bin/env python3
"""CI file scanner for AI-writing signals in the human-voice hard gate.

Takes text file paths on argv, scans each whole file, prints every finding
with its file and count, and exits 1 when any file has a finding. Exit 0
means every scanned file was clean, including the case where no text file
changed.

Relationship to the canonical scanner. The source of truth for the signal
list is ~/Code/vibe_skills/hooks/scan-ai-signals.py, which is a Claude Code
PostToolUse hook: it reads a JSON tool payload on stdin, looks only at the
text of one edit, and warns without blocking. That shape cannot run in CI,
and the vibe_skills repo is private and absent from a runner. So this file
is a deliberate vendored port with the same thresholds in a file-in,
exit-code-out shape. When the canonical list changes, update this copy in
the same change. The prose rules it encodes live in
askajay-thought-leadership/skills/_shared/ai-writing-signals.md.

Thresholds, matching the canonical hook:
  em-dash count      more than 2 in a file
  lexicon cluster    2 or more distinct terms in prose, 3 or more elsewhere
  signposts          any hit in prose
  negation tic       2 or more occurrences of "not just / only / merely"
Files under 120 characters are skipped as too short to judge.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Files that legitimately quote the banned signals (blocklists, gate docs,
# fixtures, this scanner) or are not prose at all.
SKIP_PATH = re.compile(
    r"ai-writing-signals|quality-gates|non-negotiables|scan-ai-signals|"
    r"cases\.yaml|check-consistency|\.json$|\.lock$|\.svg$|\.csv$|node_modules",
    re.I,
)

PROSE_SUFFIX = re.compile(r"\.(md|mdx|txt|rst)$", re.I)

EM_DASH_LIMIT = 2
MIN_LENGTH = 120

LEXICON = [
    "delve",
    "delves",
    "delving",
    "leverage",
    "leverages",
    "leveraging",
    "robust",
    "seamless",
    "seamlessly",
    "underscore",
    "underscores",
    "tapestry",
    "pivotal",
    "harness",
    "harnessing",
    "myriad",
    "in today's fast-paced",
    "in today's world",
    "ever-evolving",
    "game-changer",
    "elevate your",
]

SIGNPOSTS = [
    "it's worth noting",
    "it is worth noting",
    "in conclusion",
    "at the end of the day",
    "it is important to note",
    "needless to say",
    "in summary,",
]

ANTITHESIS = re.compile(r"\bnot (just|only|merely)\b", re.I)


def scan(text: str, is_prose: bool) -> list[str]:
    findings: list[str] = []

    em = text.count("—")
    if em > EM_DASH_LIMIT:
        findings.append(f"{em} em-dashes (limit {EM_DASH_LIMIT}, target 0)")

    low = text.lower()
    lex_hits = sorted({w for w in LEXICON if re.search(rf"\b{re.escape(w)}\b", low)})
    lex_floor = 2 if is_prose else 3
    if len(lex_hits) >= lex_floor:
        findings.append("AI-lexicon cluster: " + ", ".join(lex_hits[:5]))

    hits = [s for s in SIGNPOSTS if s in low]
    if hits and is_prose:
        findings.append("signpost scaffolding: " + ", ".join(hits[:3]))

    anti = len(ANTITHESIS.findall(text))
    if anti >= 2:
        findings.append(f'{anti} negation-antithesis constructions ("not just X")')

    return findings


def main(argv: list[str]) -> int:
    paths = [a for a in argv if a.strip()]
    if not paths:
        print("ai-signal-scan: no text files to scan, nothing to judge")
        return 0

    failed = False
    scanned = 0

    for raw in paths:
        path = Path(raw)
        if SKIP_PATH.search(raw):
            print(f"skip (quotes the blocklist or not prose): {raw}")
            continue
        if not path.is_file():
            print(f"ai-signal-scan: {raw} is not a readable file", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) < MIN_LENGTH:
            print(f"skip (under {MIN_LENGTH} characters): {raw}")
            continue

        scanned += 1
        findings = scan(text, bool(PROSE_SUFFIX.search(raw)))
        if findings:
            failed = True
            print(f"FAIL {raw}")
            for f in findings:
                print(f"      {f}")
        else:
            print(f"ok   {raw}")

    print(f"ai-signal-scan: {scanned} file(s) scanned")
    if failed:
        print(
            "ai-signal-scan: rewrite for human cadence. Fewer em-dashes, plain "
            "verbs, varied sentence shape. Rules: "
            "askajay-thought-leadership/skills/_shared/ai-writing-signals.md"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
