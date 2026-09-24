#!/usr/bin/env bash
set -euo pipefail

ACCESSION_TABLE="${1:-data/accessions.tsv}"
OUTDIR="${2:-data/raw}"

if ! command -v datasets >/dev/null 2>&1; then
    echo "ERROR: NCBI datasets CLI was not found in PATH." >&2
    echo "Install the Conda environment from environment.yml." >&2
    exit 1
fi

mkdir -p "${OUTDIR}"

tail -n +2 "${ACCESSION_TABLE}" | while IFS=$'\t' read -r sample_id accession strain source; do
    if [[ -z "${accession}" ]]; then
        continue
    fi

    sample_dir="${OUTDIR}/${sample_id}"
    archive="${sample_dir}/${accession}_dataset.zip"

    mkdir -p "${sample_dir}"

    echo "Downloading ${sample_id}: ${accession}"
    datasets download genome accession "${accession}" \
        --include genome,gff3,protein \
        --filename "${archive}" \
        --no-progressbar

    unzip -q -o "${archive}" -d "${sample_dir}"
done

echo "Genome download complete."
