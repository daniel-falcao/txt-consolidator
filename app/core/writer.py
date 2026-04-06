"""
Output writer.

Persists the consolidated lines to a single TXT file and returns
a simple stats object for reporting.
"""

import logging
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class WriteResult:
    """Holds statistics from a write operation."""

    output_path: Path
    lines_written: int

    def summary(self) -> str:
        """Returns a human-readable summary string."""
        return (
            f'Lines written : {self.lines_written}\n'
            f'Output file   : {self.output_path}'
        )


def write_output(
    lines: list[str],
    output_path: Path,
    encoding: str = 'utf-8',
) -> WriteResult:
    """
    Writes *lines* to *output_path*, one line per entry.

    Creates parent directories if they do not exist.

    Args:
        lines:       List of strings to write (no trailing newline needed).
        output_path: Destination file path.
        encoding:    Output file encoding (default: 'utf-8').

    Returns:
        A WriteResult with the output path and number of lines written.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding=encoding) as fh:
        for line in lines:
            fh.write(line + '\n')

    logger.info('Output saved → %s (%d lines).', output_path, len(lines))
    return WriteResult(output_path=output_path, lines_written=len(lines))
