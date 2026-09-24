#!/usr/bin/env python3
"""Calculate basic bacterial genome assembly statistics from FASTA."""

from __future__ import annotations

import argparse
from pathlib import Path

from Bio import SeqIO


def calculate_n50(lengths: list[int]) -> int:
    """Return N50 for a non-empty list of sequence lengths."""
    if not lengths:
        raise ValueError("Cannot calculate N50 for an empty sequence set.")

    total = sum(lengths)
    cumulative = 0
    for length in sorted(lengths, reverse=True):
        cumulative += length
        if cumulative >= total / 2:
            return length

    raise RuntimeError("N50 calculation failed unexpectedly.")


def calculate_stats(fasta_path: Path) -> dict[str, int | float]:
    """Calculate assembly-level statistics from a FASTA file."""
    records = list(SeqIO.parse(str(fasta_path), "fasta"))
    if not records:
        raise ValueError(f"No FASTA records found in {fasta_path}")

    sequences = [str(record.seq).upper() for record in records]
    lengths = [len(seq) for seq in sequences]

    total_length = sum(lengths)
    gc_count = sum(seq.count("G") + seq.count("C") for seq in sequences)
    atgc_count = sum(
        seq.count("A") + seq.count("T") + seq.count("G") + seq.count("C")
        for seq in sequences
    )

    gc_percent = (100.0 * gc_count / atgc_count) if atgc_count else 0.0

    return {
        "contigs": len(lengths),
        "total_length": total_length,
        "min_contig": min(lengths),
        "max_contig": max(lengths),
        "mean_contig": total_length / len(lengths),
        "n50": calculate_n50(lengths),
        "gc_percent": gc_percent,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate basic genome assembly statistics."
    )
    parser.add_argument("fasta", type=Path)
    parser.add_argument("--sample-id", default="sample")
    args = parser.parse_args()

    stats = calculate_stats(args.fasta)

    headers = [
        "sample_id",
        "contigs",
        "total_length",
        "min_contig",
        "max_contig",
        "mean_contig",
        "n50",
        "gc_percent",
    ]
    values = [
        args.sample_id,
        stats["contigs"],
        stats["total_length"],
        stats["min_contig"],
        stats["max_contig"],
        f'{stats["mean_contig"]:.2f}',
        stats["n50"],
        f'{stats["gc_percent"]:.2f}',
    ]

    print("\t".join(headers))
    print("\t".join(map(str, values)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
