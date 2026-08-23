#!/usr/bin/env python3
"""Resolve every relative markdown link and #anchor in this repository.

A broken anchor fails silently: GitHub serves the page with a 200 and ignores the fragment, so the
reader lands at the top of the file with nothing saying the link was wrong. Only a mechanical pass
finds one, and this repository has an index with 60-odd anchors.

THE SLUG RULES ARE VERIFIED AGAINST GITHUB, NOT PORTED ON FAITH. All 66 headings here were POSTed to
GitHub's own renderer (``gh api --method POST /markdown``) and the ``id="user-content-..."`` values it
generated were compared against what ``slug`` produces. Doing that caught a rule that a slugger copied
from a sibling repository got wrong, and which would have broken five anchors in the index:

    '⏱️ Time-Series Databases'  ->  '\ufe0f-time-series-databases'

**U+FE0F, VARIATION SELECTOR-16, SURVIVES.** Many emoji in these headings are a base symbol followed by
U+FE0F, which is Unicode category Mn (a nonspacing mark). GitHub's slugger deletes the symbol and keeps
the selector, so the anchor begins with an invisible character and then a hyphen. Python's ``\\w`` does
not match U+FE0F, so a ``[^\\w \\-]`` character class deletes it and produces an anchor one character
short. Zero-width joiner (U+200D) is kept for the same reason. Verified: 5 mismatches without them,
0 with.

Two other rules, both measured, and both easy to get backwards:

* TRIM ONCE, UP FRONT, then never again. A leading character that gets deleted leaves its space behind
  and that space becomes a hyphen. Trimming after the deletion loses that; not trimming at all leaves a
  trailing hyphen where the source had trailing whitespace.
* A heading that slugs to nothing gets NO anchor element from GitHub at all, so it must not be
  registered as an available anchor here.

The self-check below pins all of it. It is offline on purpose: a checker that needs the network is one
that stops being run.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEADING = re.compile(r"^#{1,6} +(.*)$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
ABSOLUTE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)

# Kept in addition to word characters, space and hyphen: see the docstring. U+FE0F is the variation
# selector that follows many emoji, U+200D the zero-width joiner that builds compound ones.
KEEP = "\ufe0f\u200d"
STRIP = re.compile("[^\\w \\-" + KEEP + "]", re.UNICODE)


def slug(heading: str) -> str:
    text = heading.strip().replace("`", "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = STRIP.sub("", text.lower())
    return text.replace(" ", "-")


SLUG_CASES = [
    # Verified against GitHub's renderer, one call per heading.
    ("\u23f1\ufe0f Time-Series Databases", "\ufe0f-time-series-databases"),
    ("\U0001f5c2\ufe0f Table & Column Definitions", "\ufe0f-table--column-definitions"),
    ("NATURAL JOIN (\u26a0\ufe0f Use with caution)", "natural-join-\ufe0f-use-with-caution"),
    ("\U0001f522 Relational Databases (SQL)", "-relational-databases-sql"),
    ("\U0001f310 Search & Analytics Engines", "-search--analytics-engines"),
    ("Most Common SQL Clauses", "most-common-sql-clauses"),
    ("Trailing space ", "trailing-space"),
]


def main() -> int:
    for heading, expected in SLUG_CASES:
        got = slug(heading)
        if got != expected:
            print(
                "slug() self-check failed: %r -> %r, expected %r" % (heading, got, expected),
                file=sys.stderr,
            )
            return 1

    files = sorted(p.name for p in ROOT.glob("*.md"))
    anchors = {}
    links = []

    for name in files:
        seen, found, in_fence = {}, set(), False
        for number, line in enumerate((ROOT / name).read_text().split("\n"), start=1):
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            heading = HEADING.match(line)
            if heading:
                base = slug(heading.group(1))
                # GitHub emits no anchor at all for a heading that slugs to nothing.
                if base.strip("-" + KEEP):
                    count = seen.get(base, 0)
                    seen[base] = count + 1
                    found.add(base if count == 0 else "%s-%d" % (base, count))
            for target in LINK.findall(line):
                if ABSOLUTE.match(target) or target.startswith("//"):
                    continue
                links.append((name, number, target))
        anchors[name] = found

    problems = []
    for source, number, target in links:
        path, _, fragment = target.partition("#")
        resolved = source if path == "" else str(pathlib.PurePath(path).name) if "/" not in path.strip("./") else path

        if path != "":
            candidate = (ROOT / path).resolve()
            if not candidate.exists():
                problems.append("%s:%d  %s\n      no such file: %s" % (source, number, target, path))
                continue
            resolved = candidate.name
            if resolved not in anchors and fragment:
                problems.append(
                    "%s:%d  %s\n      %s is not markdown, so #%s cannot resolve"
                    % (source, number, target, path, fragment)
                )
                continue
        if fragment and fragment not in anchors.get(resolved, set()):
            problems.append(
                "%s:%d  %s\n      no heading in %s with anchor #%s"
                % (source, number, target, resolved, fragment)
            )

    print("%d relative links across %d files" % (len(links), len(files)))
    sys.stdout.flush()
    if not problems:
        print("all resolve")
        return 0
    print("")
    for problem in problems:
        print("  " + problem, file=sys.stderr)
    print("\n%d broken link(s)" % len(problems), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
