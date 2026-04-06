"""
Lookup table loader.

Reads the mapping Excel file and returns a dictionary used to
translate original codes into their standardised equivalents.
"""

import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


def load_lookup(
    path: Path,
    key_col_index: int = 0,
    value_col_index: int = 2,
    sheet_name: int | str = 0,
) -> dict[str, str]:
    """
    Reads an Excel file and builds a lookup dictionary.

    The key is taken from column *key_col_index* (default: column A, index 0)
    and the value from column *value_col_index* (default: column C, index 2).
    All values are read as strings and stripped of surrounding whitespace.

    Args:
    path:            Path to the Excel file (.xlsx or .xls).
    key_col_index:   0-based column index used as the dictionary key.
    value_col_index: 0-based column index used as the dictionary value.
    sheet_name:      Sheet name or 0-based index to read (default: first sheet)

    Returns:
        A dict mapping key strings to value strings.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError:        If the file has fewer columns than required.
    """
    if not path.exists():
        raise FileNotFoundError(f'Lookup file not found: {path}')

    logger.info('Loading lookup table from %s …', path.name)

    df = pd.read_excel(path, sheet_name=sheet_name, dtype=str)
    df = df.fillna('')

    required_cols = max(key_col_index, value_col_index) + 1
    if df.shape[1] < required_cols:
        raise ValueError(
            f'Lookup file has only {df.shape[1]} column(s); '
            f'at least {required_cols} required.'
        )

    lookup: dict[str, str] = {
        str(row.iloc[key_col_index]).strip(): str(row.iloc[value_col_index]
                                                  ).strip()
        for _, row in df.iterrows()
        if str(row.iloc[key_col_index]).strip()
    }

    logger.info('Lookup table loaded — %d entries.', len(lookup))
    return lookup
