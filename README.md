# Helicobacter pylori Genomics

A reproducible research repository for comparative genomic analysis of *Helicobacter pylori* using public genome data.

The project is designed as a transparent starting point for bacterial-genomics analyses involving genome retrieval, assembly-level quality summaries, metadata integration, virulence-associated loci, antimicrobial-resistance determinants, and phylogenetic analysis.

## Scientific Scope

The repository is organized around four biological questions:

1. What is the genomic diversity represented by a defined set of *H. pylori* isolates?
2. How are virulence-associated loci distributed across genomes?
3. Which known antimicrobial-resistance-associated variants are present?
4. How do genomic differences relate to phylogenetic structure and available isolate metadata?

The initial release implements the reproducible data-ingestion and genome-summary layer. Virulence, AMR, and phylogenetic modules can be added without changing the project structure.

## Data Policy

Only public genomic records or non-identifiable example metadata should be committed to this repository.

Do **not** commit:

- patient identifiers;
- clinical record numbers;
- unpublished institutional datasets;
- raw confidential sequencing data;
- credentials or API keys.

The included accession table contains the public *H. pylori* 26695 reference assembly as a demonstration record.

## Repository Structure

```text
helicobacter-pylori-genomics/
├── README.md
├── LICENSE
├── CITATION.cff
├── environment.yml
├── requirements.txt
├── .gitignore
├── config/
│   └── config.yaml
├── data/
│   ├── README.md
│   └── accessions.tsv
├── metadata/
│   └── metadata_template.tsv
├── scripts/
│   ├── fetch_ncbi_genomes.sh
│   ├── validate_accessions.py
│   └── assembly_stats.py
├── tests/
│   ├── test_assembly_stats.py
│   └── fixtures/
│       └── test_contigs.fasta
├── docs/
│   └── workflow.md
├── results/
│   └── .gitkeep
└── figures/
    └── .gitkeep
```

## Requirements

The recommended setup uses Conda or Mamba.

```bash
conda env create -f environment.yml
conda activate hpylori-genomics
```

A lightweight Python-only installation is also possible:

```bash
python -m pip install -r requirements.txt
```

The NCBI Datasets command-line tool is required for downloading public genome packages.

Official documentation:

- NCBI Datasets: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/
- Genome download command: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/command-line/datasets/download/genome/

## 1. Validate the accession table

```bash
python scripts/validate_accessions.py data/accessions.tsv
```

The script checks for:

- required columns;
- missing accessions;
- duplicate accessions;
- basic NCBI assembly-accession formatting.

## 2. Download public genome data

The shell script reads assembly accessions from `data/accessions.tsv` and uses the NCBI Datasets CLI.

```bash
bash scripts/fetch_ncbi_genomes.sh
```

Genome packages are written under `data/raw/`, which is excluded from Git tracking.

## 3. Calculate assembly statistics

For an individual FASTA file:

```bash
python scripts/assembly_stats.py \
  path/to/genome.fna \
  --sample-id strain_26695
```

The output contains:

- number of contigs;
- total assembly length;
- minimum and maximum contig length;
- mean contig length;
- N50;
- GC percentage.

Example tabular output can be redirected to a file:

```bash
python scripts/assembly_stats.py genome.fna --sample-id strain_26695 \
  > results/assembly_stats.tsv
```

## Testing

Run:

```bash
pytest -q
```

The tests use a small synthetic FASTA fixture and do not contain patient or research data.

## Planned Analysis Modules

Subsequent releases can add:

- genome quality filtering;
- standardized genome annotation;
- virulence-associated gene screening;
- analysis of *cagA* and *vacA* sequence diversity;
- AMR-associated variant detection;
- core-genome or SNP-based phylogenetics;
- population-genomic metadata integration;
- publication-quality visualizations.

Each biological module should document its reference database, software version, thresholds, and interpretation criteria.

## Reference Genome

The demonstration accession is the public *Helicobacter pylori* 26695 genome assembly:

- NCBI BioProject: PRJNA233
- GenBank assembly: GCA_000008525.1

See: https://www.ncbi.nlm.nih.gov/bioproject/233

## Reproducibility

The repository separates:

- public accession lists from downloaded sequence files;
- source code from generated results;
- test fixtures from biological datasets;
- configuration from analysis logic.

Large downloaded genomic files and generated intermediate outputs should not be committed to Git.

## Citation

If you reuse this repository, cite the software using `CITATION.cff` and cite the original genomic records and biological databases used in your analysis.

## License

Code is released under the MIT License. Public biological data remain subject to the terms of their original repositories and sources.
