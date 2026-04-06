"""
txt-consolidator — entry point.

Run:
    python run_consolidate.py

All configuration is in config.py.
"""

import logging
import sys

import config
from app.core.lookup import load_lookup
from app.core.consolidator import consolidate_files
from app.core.writer import write_output
from app.utils.logger import setup_logging


def main() -> None:
    """
    Orchestrates the full consolidation pipeline:

    1. Configure logging.
    2. Load the lookup table from the Excel file.
    3. Consolidate all source TXT files using the lookup map.
    4. Write the enriched output to disk.
    5. Print a run summary.
    """
    setup_logging(config.LOG_FILE)
    logger = logging.getLogger(__name__)
    logger.info('==== txt-consolidator started ====')

    try:
        lookup_map = load_lookup(
            path=config.LOOKUP_FILE,
            key_col_index=config.KEY_COL_INDEX,
            value_col_index=config.VALUE_COL_INDEX,
            sheet_name=config.LOOKUP_SHEET,
        )

        lines = consolidate_files(
            input_folder=config.INPUT_FOLDER,
            lookup_map=lookup_map,
            code_field_index=config.CODE_FIELD_INDEX,
            delimiter=config.DELIMITER,
            encoding=config.INPUT_ENCODING,
            file_glob=config.FILE_GLOB,
        )

        result = write_output(lines=lines, output_path=config.OUTPUT_FILE)

        logger.info('==== Run complete ====')
        print('\n' + result.summary())

    except FileNotFoundError as exc:
        logger.error(str(exc))
        print(f'\nError: {exc}')
        sys.exit(1)
    except Exception as exc:
        logger.error('Unexpected error: %s', exc, exc_info=True)
        print(f'\nUnexpected error: {exc}')
        sys.exit(1)


if __name__ == '__main__':
    main()
