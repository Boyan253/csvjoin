#!/usr/bin/env python3
"""Join two CSV files on a key column: inner, left or outer."""

import argparse
import csv
import sys

__version__ = "0.1.0"


def index_by(rows, key):
    """Group rows by key value, preserving duplicates."""
    out = {}
    for row in rows:
        out.setdefault(row.get(key, ""), []).append(row)
    return out


def merged_fields(left_fields, right_fields, key, suffix):
    fields = list(left_fields)
    for name in right_fields:
        if name == key:
            continue
        fields.append(name + suffix if name in left_fields else name)
    return fields


def join(left_rows, right_rows, key, how="inner", suffix="_r"):
    left_rows = list(left_rows)
    right_rows = list(right_rows)
    if not left_rows:
        return [], []
    left_fields = list(left_rows[0].keys())
    right_fields = list(right_rows[0].keys()) if right_rows else []
    fields = merged_fields(left_fields, right_fields, key, suffix)
    right_index = index_by(right_rows, key)
    seen = set()
    out = []

    for row in left_rows:
        matches = right_index.get(row.get(key, ""), [])
        seen.add(row.get(key, ""))
        if not matches:
            if how in ("left", "outer"):
                out.append({**row})
            continue
        for match in matches:
            merged = dict(row)
            for name, value in match.items():
                if name == key:
                    continue
                merged[name + suffix if name in left_fields else name] = value
            out.append(merged)

    if how == "outer":
        for value, rows in right_index.items():
            if value in seen:
                continue
            for match in rows:
                out.append({key: value, **{k: v for k, v in match.items() if k != key}})
    return fields, out


def read_csv(path, delimiter):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=delimiter))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("left")
    ap.add_argument("right")
    ap.add_argument("-k", "--key", required=True, help="column present in both files")
    ap.add_argument("--how", default="inner", choices=["inner", "left", "outer"])
    ap.add_argument("--suffix", default="_r", help="suffix for clashing right-hand columns")
    ap.add_argument("-d", "--delimiter", default=",")
    args = ap.parse_args(argv)

    left = read_csv(args.left, args.delimiter)
    right = read_csv(args.right, args.delimiter)
    fields, rows = join(left, right, args.key, args.how, args.suffix)
    if not fields:
        return 0
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, delimiter=args.delimiter,
                            lineterminator="\n", restval="")
    writer.writeheader()
    writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
