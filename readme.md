# PubMed Fetcher CLI

This tool fetches research papers from PubMed based on a user-supplied query, identifies papers with non-academic authors (pharmaceutical/biotech), and exports the results as a CSV.

## 📦 Installation

```bash
poetry install
##Tools Used
This project uses:

Biopython for the PubMed API

pandas for CSV formatting

Poetry for packaging

argparse for CLI

regex for email detection
