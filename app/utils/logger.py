"""
Centralised logger setup.

Writes INFO+ to the console and DEBUG+ to an optional log file.
Call setup_logging() once at application startup.
"""

import logging
import os
from pathlib import Path


def setup_logging(log_file: Path | str | None = None) -> None:
    """
    Configures the root logger with a console handler and an optional
    file handler.

    Args:
        log_file: Path to the log file. If None, falls back to the
                  LOG_FILE environment variable. File logging is skipped
                  when neither is set.
    """
    fmt = logging.Formatter(
        '%(asctime)s — %(levelname)s — %(name)s — %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if not root.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)
        root.addHandler(ch)

    target = log_file or os.getenv('LOG_FILE')
    if target:
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(target, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        root.addHandler(fh)
