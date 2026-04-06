"""
================================================================
  txt-consolidator — CONFIGURATION FILE
  Edit the values below to match your environment.
  No other file needs to change.
================================================================

WORKFLOW
--------
  1. The tool scans INPUT_FOLDER for all files matching FILE_GLOB.
  2. For each row it reads the field at CODE_FIELD_INDEX (0-based).
  3. That code is looked up in LOOKUP_FILE:
       - KEY_COL_INDEX   → column whose value matches the code (default: A = 0)
       - VALUE_COL_INDEX → column whose value becomes new_code (default: C = 2)
  4. The new_code is appended as a new field and the enriched row
     is written to OUTPUT_FILE.
  5. A log is written to LOG_FILE.

FIELD INDEX REFERENCE
---------------------
  Fields in a semicolon-delimited row are 0-based:
    field 0 ; field 1 ; field 2 ; field 3 ; field 4 ; ...
  The original script used field 4 (the 5th field) as the code.
  Change CODE_FIELD_INDEX if your files use a different position.
"""

from pathlib import Path

# ── Folders ─────────────────────────────────────────────────────────────

# Folder that contains the source TXT files
INPUT_FOLDER: Path = Path('data/input')

# Excel file with the code-mapping table
LOOKUP_FILE: Path = Path('data/lookup/domain.xlsx')

# Where the consolidated output file will be saved
OUTPUT_FILE: Path = Path('data/output/consolidated.txt')

# Log file path (set to None to disable file logging)
LOG_FILE: Path | None = Path('logs/run.log')


# ── Source file settings ────────────────────────────────────────────────

# Glob pattern for selecting input files (case-insensitive on most systems)
FILE_GLOB: str = '*.txt'

# Delimiter used in the source TXT files
DELIMITER: str = ';'

# Encoding of the source TXT files
INPUT_ENCODING: str = 'utf-8'

# 0-based index of the field used as the lookup key
# Example: CODE_FIELD_INDEX = 4  →  the 5th semicolon-delimited field
CODE_FIELD_INDEX: int = 4


# ── Lookup table settings (domain.xlsx) ─────────────────────────────────

# 0-based column index in the Excel file that holds the original code (key)
# Default: 0  →  column A
KEY_COL_INDEX: int = 0

# 0-based column index in the Excel file that holds the new code (value)
# Default: 2  →  column C
VALUE_COL_INDEX: int = 2

# Sheet to read from the Excel file (0 = first sheet, or use sheet name)
LOOKUP_SHEET: int | str = 0
