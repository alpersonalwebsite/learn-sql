#!/usr/bin/env python3
"""Run the SQL in these notes against the sample data the notes themselves define, and compare the
results against the tables the notes claim they produce.

This is the only check here worth automating, because a SQL sample in a markdown file has two ways to
be wrong and both are invisible on reading:

1. The query does not run at all. Two in this repository did not, against the schema defined a few
   lines above them.
2. The query runs and returns something other than what the document says it returns. The document's
   own sample data changed at some point and three result tables plus a prose sentence were left
   describing the old data.

HOW IT WORKS. Sample tables are parsed out of the markdown, loaded into an in-memory sqlite database,
each ```sql block is executed, and the rows that come back are diffed against the result table that
follows it. Tables are scoped PER SECTION: a heading starts a fresh database seeded with the
document-level tables plus any table defined under that heading. Without that, the two different
`employees` tables in the joins document (one with manager_id, one with department_id) would collide.

ROW ORDER IS COMPARED ONLY WHEN THE QUERY HAS AN ORDER BY. Without one SQL promises nothing about
order, so a document listing rows in a particular sequence is describing one possible output rather
than the only correct one, and comparing as multisets is the honest reading. With an ORDER BY the
sequence IS the claim, so it is compared position by position.

That detection is a regex on the statement with comments stripped, which is a heuristic and not a
parser: an ORDER BY inside a subquery would trip it, and no sample here has one. It is deliberately
biased toward the strict comparison, because being too strict produces a failure to read while being
too loose silently accepts a wrong sequence.

Where a documented table is truncated with a `...` row, the listed rows are checked as a SUBSET and the
real total is reported.

SQLITE IS NOT EVERY DIALECT, and that limits what a failure here means. These notes cover MySQL,
Postgres and SQL Server too, so a block using a dialect-specific function is expected to fail and says
so on its first line:

    -- check: fails <text>    this query is SUPPOSED to fail, and the error must contain <text>
    -- check: fragment        a clause or column definition, not a standalone statement
    -- check: dialect <name>   not portable to sqlite; execution is not attempted
    -- check: notation         not SQL at all (a diagram, a schema sketch)

Those are kept distinct rather than folded into one "skip", because they are different claims. A
fragment IS valid SQL in the right context; a dialect block is valid SQL that sqlite cannot run; a
notation block is not SQL at all and mislabelling it as ```sql is itself the defect.

`dialect` has no users in this repository today. The two blocks that ARE dialect-specific
(`IDENTITY(1,1)`, `AUTO_INCREMENT`) are column definitions, so `fragment` is the accurate marker for
them and this one is waiting for a standalone statement that sqlite rejects on dialect grounds. Noted
because the paragraph above argues these categories are distinct claims, and a category making no
claim about anything should say so.

`fails` is the opposite of a skip and the most useful of the four: a query shown in order to
demonstrate an error is otherwise indistinguishable from a query that is simply broken, and this turns
"this does not work" from a sentence into something enforced. If such a query ever starts succeeding,
or fails with a different message, that is a failure here.

First line only, and only as a comment. That is deliberately tighter than honouring the marker
anywhere: a marker that can be attached to the offending line turns an exemption into an off switch
reachable from inside the thing being checked.

Standard library only: sqlite3 ships with Python.
"""

from __future__ import annotations

import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

FENCE_OPEN = re.compile(r"^```(\w+)?\s*$")
FENCE_CLOSE = "```"
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
MARKER = re.compile(r"^--\s*check:\s*(notation|fragment|dialect\s+\S+|fails\s+.+)\s*$")
# A markdown table row, and the separator under a header.
ROW = re.compile(r"^\s*\|(.+)\|\s*$")
SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
# An ASCII box-drawing table, which one section in the joins document uses instead.
BOX_EDGE = re.compile(r"^\s*\+[-+]+\+\s*$")
# A bare line naming a table, optionally prefixed with an emoji or other symbol.
LABEL = re.compile(r"^[^\w`]*([a-z_][a-z0-9_]*)\s*$", re.IGNORECASE)


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse(path: pathlib.Path):
    """Walk one file, yielding events in document order."""
    lines = path.read_text().split("\n")
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        heading = HEADING.match(line)
        if heading:
            yield ("heading", index + 1, len(heading.group(1)), heading.group(2))
            index += 1
            continue

        opening = FENCE_OPEN.match(stripped)
        if opening:
            lang = opening.group(1)
            body: list[str] = []
            start = index + 2
            index += 1
            while index < len(lines) and lines[index].strip() != FENCE_CLOSE:
                body.append(lines[index])
                index += 1
            index += 1
            yield ("fence", start, lang, body)
            continue

        # A markdown table: a row, then a separator.
        if ROW.match(line) and index + 1 < len(lines) and SEP.match(lines[index + 1]):
            header = cells(line)
            start = index + 1
            index += 2
            rows = []
            while index < len(lines) and ROW.match(lines[index]):
                rows.append(cells(lines[index]))
                index += 1
            yield ("table", start, header, rows)
            continue

        # An ASCII box table: +---+, header, +---+, rows, +---+
        if BOX_EDGE.match(line) and index + 1 < len(lines) and ROW.match(lines[index + 1]):
            start = index + 1
            index += 1
            collected = []
            while index < len(lines) and (ROW.match(lines[index]) or BOX_EDGE.match(lines[index])):
                if ROW.match(lines[index]):
                    collected.append(cells(lines[index]))
                index += 1
            if collected:
                yield ("boxtable", start, collected[0], collected[1:])
            continue

        label = LABEL.match(stripped) if stripped else None
        if label:
            yield ("label", index + 1, label.group(1), None)
        index += 1
    return


def column_type(values: list[str]) -> str:
    real = ints = 0
    for value in values:
        if value.upper() == "NULL" or value == "":
            continue
        try:
            int(value)
            ints += 1
        except ValueError:
            try:
                float(value)
                real += 1
            except ValueError:
                return "TEXT"
    if real:
        return "REAL"
    return "INTEGER" if ints else "TEXT"


def coerce(value: str):
    return None if value.upper() == "NULL" or value == "" else value


def create(db: sqlite3.Connection, name: str, header: list[str], rows: list[list[str]]) -> None:
    columns = [re.sub(r"\W", "_", h.lower()) for h in header]
    types = [column_type([r[i] for r in rows if i < len(r)]) for i in range(len(columns))]
    spec = ", ".join('"%s" %s' % (c, t) for c, t in zip(columns, types))
    db.execute('CREATE TABLE "%s" (%s)' % (name, spec))
    placeholders = ", ".join("?" * len(columns))
    for row in rows:
        padded = (row + [""] * len(columns))[: len(columns)]
        db.execute(f'INSERT INTO "{name}" VALUES ({placeholders})', [coerce(v) for v in padded])
    db.commit()


def normalise(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value).strip()


def main() -> int:
    failures = []
    executed = skipped_notation = skipped_fragment = skipped_dialect = compared = no_result = 0
    expected_failures = 0

    for path in sorted(ROOT.glob("*.md")):
        # Group events into sections. A level-3 heading (or deeper) opens a new scope; tables defined
        # before the first one are document-level and visible everywhere in the file.
        document_tables = []
        sections = []           # each: {"tables": [...], "queries": [(line, sql, result_or_None)]}
        current = None
        pending_label = None
        awaiting_result_for = None

        for event in parse(path):
            kind, line = event[0], event[1]

            if kind == "heading":
                if event[2] >= 3:
                    current = {"tables": [], "queries": []}
                    sections.append(current)
                pending_label, awaiting_result_for = None, None
                continue

            if kind == "label":
                pending_label = event[2]
                continue

            if kind in ("table", "boxtable"):
                header, rows = event[2], event[3]
                if pending_label is not None:
                    entry = (pending_label, header, rows)
                    (current["tables"] if current else document_tables).append(entry)
                    pending_label = None
                    continue
                # An unlabelled table right after a query is that query's documented result.
                if awaiting_result_for is not None:
                    queries = (current or {"queries": []})["queries"]
                    index = awaiting_result_for
                    q = queries[index]
                    queries[index] = (q[0], q[1], (line, header, rows), q[3])
                    awaiting_result_for = None
                continue

            if kind == "fence":
                lang, body = event[2], event[3]
                if lang != "sql":
                    continue
                first = body[0].strip() if body else ""
                mark = MARKER.match(first)
                expect_failure = None
                if mark:
                    which = mark.group(1)
                    if which.startswith("fails "):
                        expect_failure = which[6:].strip()
                    elif which == "notation":
                        skipped_notation += 1
                        awaiting_result_for = None
                        continue
                    elif which == "fragment":
                        skipped_fragment += 1
                        awaiting_result_for = None
                        continue
                    else:
                        skipped_dialect += 1
                        awaiting_result_for = None
                        continue
                sql = "\n".join(body).strip()
                if not sql:
                    continue
                if current is None:
                    current = {"tables": [], "queries": []}
                    sections.append(current)
                current["queries"].append((line, sql, None, expect_failure))
                awaiting_result_for = len(current["queries"]) - 1
                continue

        # Now execute. Tables are collected for the WHOLE section first, so a query works whether the
        # sample data is shown above it or below it: the joins document does both.
        for section in sections:
            for query_line, sql, result, expect_failure in section["queries"]:
                executed += 1
                db = sqlite3.connect(":memory:")
                error_text = None
                actual = None
                try:
                    for name, header, rows in document_tables + section["tables"]:
                        create(db, name, header, rows)
                    actual = [[normalise(v) for v in row] for row in db.execute(sql).fetchall()]
                except sqlite3.Error as error:
                    error_text = str(error)
                finally:
                    db.close()

                if expect_failure is not None:
                    if error_text is None:
                        failures.append(
                            "EXPECTED FAILURE %s:%d  marked to fail with %r, but it succeeded"
                            % (path.name, query_line, expect_failure)
                        )
                    elif expect_failure.lower() not in error_text.lower():
                        failures.append(
                            "WRONG FAILURE %s:%d  marked to fail with %r, got: %s"
                            % (path.name, query_line, expect_failure, error_text)
                        )
                    else:
                        expected_failures += 1
                    continue

                if error_text is not None:
                    failures.append("SQL ERROR %s:%d  %s" % (path.name, query_line, error_text))
                    continue

                if result is None:
                    no_result += 1
                    continue

                compared += 1
                table_line, header, rows = result
                truncated = bool(rows) and all(c.strip(". ") == "" for c in rows[-1])
                documented = rows[:-1] if truncated else rows
                width = len(header)
                doc_rows = [tuple((r + [""] * width)[:width]) for r in documented]
                act_rows = [tuple((r + [""] * width)[:width]) for r in actual]

                if truncated:
                    missing = [r for r in doc_rows if r not in act_rows]
                    if missing:
                        failures.append(
                            "RESULT %s:%d  %d documented row(s) absent from the actual result "
                            "(truncated table; %d rows returned): %s"
                            % (path.name, table_line, len(missing), len(act_rows), missing[:3])
                        )
                    continue

                bare = re.sub(r"--[^\n]*", "", sql)
                ordered = re.search(r"\border\s+by\b", bare, re.IGNORECASE) is not None

                if ordered:
                    if doc_rows != act_rows:
                        failures.append(
                            "ORDER %s:%d  the query has an ORDER BY, so the sequence is the claim. "
                            "documented %s, actual %s"
                            % (path.name, table_line, doc_rows[:4], act_rows[:4])
                        )
                    continue

                if sorted(doc_rows) != sorted(act_rows):
                    only_doc = [r for r in doc_rows if r not in act_rows]
                    only_act = [r for r in act_rows if r not in doc_rows]
                    detail = []
                    if only_doc:
                        detail.append("documented but not returned: %s" % (only_doc[:3],))
                    if only_act:
                        detail.append("returned but not documented: %s" % (only_act[:3],))
                    failures.append(
                        "RESULT %s:%d  %d documented vs %d actual. %s"
                        % (path.name, table_line, len(doc_rows), len(act_rows), "; ".join(detail))
                    )

    print(
        "%d sql blocks executed, %d compared against a documented result table, %d with none to compare"
        % (executed, compared, no_result)
    )
    print(
        "  skipped: %d marked fragment, %d marked notation, %d marked dialect-specific"
        % (skipped_fragment, skipped_notation, skipped_dialect)
    )
    print("  %d query(ies) failed as documented" % expected_failures)
    sys.stdout.flush()

    if not failures:
        print("no failures")
        return 0

    print("")
    for failure in failures:
        print("  " + failure, file=sys.stderr)
    print("\n%d failure(s)" % len(failures), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
