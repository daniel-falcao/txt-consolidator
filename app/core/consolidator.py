"""
Core consolidation logic.

Reads multiple TXT files from a folder, maps a code field against
an Excel lookup table, and returns the enriched lines ready for output.
"""

import logging
from pathlib import Path

from tqdm import tqdm


logger = logging.getLogger(__name__)


def consolidate_files(input_folder: Path, lookup_map: dict[str, str],
                      code_field_index: int = 4, delimiter: str = ';',
                      encoding: str = 'utf-8', file_glob: str = '*.txt',
                      ) -> list[str]:
    """
    Reads all TXT files matching *file_glob* inside *input_folder*,
    appends a new_code field to each row by looking up the value at
    *code_field_index* in *lookup_map*, and returns the enriched lines.

    Args:
    input_folder:     Directory containing the source TXT files.
    lookup_map:       Dict mapping original codes to their equivalents.
    code_field_index: 0-based index of the code field in each row (default 4).
    delimiter:        Field separator used in the source files (default ';').
    encoding:         File encoding (default 'utf-8').
    file_glob:        Glob pattern to select files (default '*.txt').

    Returns:
        A list of strings, one per valid input row, with the new_code appended.

    Raises:
        FileNotFoundError: If *input_folder* does not exist.
    """
    if not input_folder.exists():
        raise FileNotFoundError(f'Input folder not found: {input_folder}')

    txt_files = sorted(input_folder.glob(file_glob))
    logger.info('Found %d file(s) in %s.', len(txt_files), input_folder)

    if not txt_files:
        logger.warning('No files matched pattern "%s" in %s.',
                       file_glob, input_folder)
        return []

    output_lines: list[str] = []
    total_skipped = 0

    for file_path in tqdm(txt_files, desc='Processing files', unit='file'):
        logger.info('Processing: %s', file_path.name)
        skipped = 0

        with open(file_path, encoding=encoding, errors='ignore') as fh:
            for raw_line in fh:
                line = raw_line.strip()

                if not line:
                    continue

                fields = line.split(delimiter)

                if len(fields) <= code_field_index:
                    logger.warning(
                        'Skipped line in %s (expected >%d fields, got %d): %s',
                        file_path.name, code_field_index, len(fields), line,
                    )
                    skipped += 1
                    continue

                code = fields[code_field_index].strip()
                new_code = lookup_map.get(code, '')
                fields.append(new_code)
                output_lines.append(delimiter.join(fields))

        if skipped:
            logger.warning('%s: %d line(s) skipped.', file_path.name, skipped)
        total_skipped += skipped

    logger.info(
        'Consolidation complete. %d line(s) processed, %d skipped.',
        len(output_lines), total_skipped,
    )
    return output_lines
