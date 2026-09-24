#!/usr/bin/env python3
"""Validate the public genome accession table."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"sample_id", "assembly_accession", "strain", "source"}
ASSEMBLY_PATTERN = re.compile(r"^GC[AF]_\d+\.\d+$")


def validate_table(path: Path) -> list[str]:
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    errors: list[str] = []

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        errors.append(
            "Missing required columns: " + ", ".join(sorted(missing_columns))
        )
        return errors

    if df.empty:
        errors.append("Accession table contains no records.")
        return errors

    for column in ("sample_id", "assembly_accession"):
        empty_rows = df.index[df[column].str.strip().eq("")].tolist()
        if empty_rows:
            errors.append(
                f"Empty {column} values at data row(s): "
                + ", ".join(str(i + 2) for i in empty_rows)
            )

    duplicated = df.loc[
        df["assembly_accession"].duplicated(keep=False), "assembly_accession"
    ].unique()
    if len(duplicated):
        errors.append(
            "Duplicate assembly accession(s): " + ", ".join(sorted(duplicated))
        )

    invalid = sorted(
        accession
        for accession in df["assembly_accession"].str.strip().unique()
        if accession and not ASSEMBLY_PATTERN.fullmatch(accession)
    )
    if invalid:
        errors.append(
            "Invalid assembly accession format: " + ", ".join(invalid)
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an NCBI assembly-accession table."
    )
    parser.add_argument("table", type=Path)
    args = parser.parse_args()

    errors = validate_table(args.table)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {args.table} passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
