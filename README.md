# txt-consolidator

> Merge multiple TXT files into one, enrich each row with a mapped code from an Excel lookup table.

[![CI](https://github.com/YOUR_USERNAME/txt-consolidator/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/txt-consolidator/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**txt-consolidator** solves a common data preparation task: you have a folder of semicolon-delimited TXT files that need to be merged into a single file, with each row enriched by a standardised code looked up from a reference Excel table.

```
data/input/*.txt  +  data/lookup/domain.xlsx  →  data/output/consolidated.txt
```

For every row the tool reads a code field, looks it up in the mapping table, and appends the translated value as a new `new_code` field. Rows whose code has no match receive an empty field — nothing is discarded.

---

## Features

| Feature | Details |
|---|---|
| Multi-file merge | Processes all `.txt` files in a folder in one run |
| Excel lookup | Maps codes via a configurable key→value column pair in `.xlsx` |
| Progress bar | Per-file progress displayed with `tqdm` |
| Detailed logging | Timestamped log to console and optional log file |
| Skip & warn | Rows with too few fields are skipped with a warning instead of crashing |
| Zero-flag config | All settings live in a single `config.py` |
| CI-ready | GitHub Actions workflow + pytest suite included |

---

## Project Structure

```
txt-consolidator/
│
├── app/
│   ├── core/
│   │   ├── consolidator.py  # File reading, field extraction, lookup
│   │   ├── lookup.py        # Excel lookup table loader
│   │   └── writer.py        # Output file writer + WriteResult stats
│   └── utils/
│       └── logger.py        # Centralised logging setup
│
├── tests/
│   └── test_core.py         # Unit tests (pytest)
│
├── sample_data/             # Example input file for quick testing
│
├── .github/
│   └── workflows/ci.yml     # GitHub Actions CI
│
├── config.py                # ← EDIT THIS to configure your run
├── run_consolidate.py       # Entry point
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/txt-consolidator.git
cd txt-consolidator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Place your TXT files in `data/input/` and your lookup Excel in `data/lookup/domain.xlsx`, then:

```bash
python run_consolidate.py
```

The consolidated file is saved to `data/output/consolidated.txt`.

---

## Configuration

All settings are in **`config.py`**.

```python
INPUT_FOLDER     = Path('data/input')          # folder with source TXT files
LOOKUP_FILE      = Path('data/lookup/domain.xlsx')
OUTPUT_FILE      = Path('data/output/consolidated.txt')
LOG_FILE         = Path('logs/run.log')        # set to None to disable

FILE_GLOB        = '*.txt'                     # pattern for file selection
DELIMITER        = ';'                         # field separator in source files
INPUT_ENCODING   = 'utf-8'
CODE_FIELD_INDEX = 4                           # 0-based index of the code field

KEY_COL_INDEX    = 0                           # Excel column A → lookup key
VALUE_COL_INDEX  = 2                           # Excel column C → new_code value
LOOKUP_SHEET     = 0                           # first sheet (or use sheet name)
```

### Lookup file format

The Excel file must have at least three columns. By default:

| Column A (index 0) | Column B (index 1) | Column C (index 2) |
|---|---|---|
| original code (key) | *(ignored)* | new_code (value) |

Change `KEY_COL_INDEX` and `VALUE_COL_INDEX` in `config.py` if your file uses different columns.

---

## Output

The output file is a merged, semicolon-delimited TXT with one extra field appended to each row:

```
REC001;2025-01-10;DEPT_A;REGION_1;CODE_X;some description;NEW_X
REC002;2025-01-11;DEPT_B;REGION_2;CODE_Y;another description;NEW_Y
REC003;2025-01-12;DEPT_A;REGION_1;CODE_UNKNOWN;no match;
```

A run summary is printed to the console:

```
Lines written : 1842
Output file   : data/output/consolidated.txt
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Requirements

- Python 3.11+
- pandas, openpyxl, tqdm

```bash
pip install -r requirements.txt
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
