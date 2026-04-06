"""
Unit tests for the txt-consolidator core modules.
Run with: pytest tests/ -v
"""

from pathlib import Path
import pandas as pd
import pytest

from app.core.lookup import load_lookup
from app.core.consolidator import consolidate_files
from app.core.writer import write_output


# ── load_lookup ─────────────────────────────────────────────────────────

def test_load_lookup_basic(tmp_path):
    """Should return a dict keyed on column A with values from column C."""

    path = tmp_path / 'domain.xlsx'
    df = pd.DataFrame({
        'code':  ['A001', 'B002', 'C003'],
        'label': ['Alpha', 'Beta', 'Gamma'],
        'new':   ['X1', 'X2', 'X3'],
    })
    df.to_excel(path, index=False)

    result = load_lookup(path, key_col_index=0, value_col_index=2)
    assert result == {'A001': 'X1', 'B002': 'X2', 'C003': 'X3'}


def test_load_lookup_missing_file():
    """Should raise FileNotFoundError when file does not exist."""
    with pytest.raises(FileNotFoundError):
        load_lookup(Path('nonexistent.xlsx'))


def test_load_lookup_too_few_columns(tmp_path):
    """Should raise ValueError when the file has fewer columns than needed."""

    path = tmp_path / 'tiny.xlsx'
    pd.DataFrame({'A': ['1', '2']}).to_excel(path, index=False)

    with pytest.raises(ValueError, match='column'):
        load_lookup(path, key_col_index=0, value_col_index=2)


# ── consolidate_files ───────────────────────────────────────────────────

def _write_txt(path: Path, lines: list[str]) -> None:
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def test_consolidate_appends_new_code(tmp_path):
    """Valid rows should have their new_code appended correctly."""
    _write_txt(tmp_path / 'a.txt', ['f0;f1;f2;f3;CODE1', 'f0;f1;f2;f3;CODE2'])
    lookup = {'CODE1': 'NEW_A', 'CODE2': 'NEW_B'}

    result = consolidate_files(tmp_path, lookup, code_field_index=4)

    assert result[0].endswith(';NEW_A')
    assert result[1].endswith(';NEW_B')


def test_consolidate_empty_new_code_when_not_found(tmp_path):
    """Rows whose code is absent from the lookup should
    get an empty new_code."""
    _write_txt(tmp_path / 'a.txt', ['f0;f1;f2;f3;UNKNOWN'])
    result = consolidate_files(tmp_path, {}, code_field_index=4)
    assert result[0].endswith(';')


def test_consolidate_skips_rows_with_too_few_fields(tmp_path):
    """Rows with fewer fields than code_field_index should be skipped."""
    _write_txt(tmp_path / 'a.txt', ['only;three;fields', 'f0;f1;f2;f3;CODE1'])
    lookup = {'CODE1': 'X'}
    result = consolidate_files(tmp_path, lookup, code_field_index=4)
    assert len(result) == 1


def test_consolidate_skips_empty_lines(tmp_path):
    """Blank lines should be ignored."""
    _write_txt(tmp_path / 'a.txt', ['', 'f0;f1;f2;f3;CODE1', ''])
    result = consolidate_files(tmp_path, {'CODE1': 'X'}, code_field_index=4)
    assert len(result) == 1


def test_consolidate_missing_folder():
    """Should raise FileNotFoundError for a non-existent input folder."""
    with pytest.raises(FileNotFoundError):
        consolidate_files(Path('no/such/folder'), {})


def test_consolidate_multiple_files(tmp_path):
    """Lines from all matching files should be merged into one list."""
    _write_txt(tmp_path / 'a.txt', ['f0;f1;f2;f3;C1'])
    _write_txt(tmp_path / 'b.txt', ['f0;f1;f2;f3;C2'])
    result = consolidate_files(tmp_path, {'C1': 'X', 'C2': 'Y'},
                               code_field_index=4)
    assert len(result) == 2


# ── write_output ────────────────────────────────────────────────────────

def test_write_output_creates_file(tmp_path):
    """Output file should be created with the correct number of lines."""
    out = tmp_path / 'sub' / 'out.txt'
    result = write_output(['line one', 'line two'], out)

    assert out.exists()
    assert result.lines_written == 2
    assert out.read_text(encoding='utf-8').count('\n') == 2


def test_write_output_summary_contains_path(tmp_path):
    """Summary string should include the output path."""
    out = tmp_path / 'out.txt'
    result = write_output(['a'], out)
    assert str(out) in result.summary()
