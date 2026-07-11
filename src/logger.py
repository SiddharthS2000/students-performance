from __future__ import annotations

import logging
from datetime import UTC, datetime

from src.config import LOGS_DIR


def _configure_root_logger() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"{datetime.now(UTC).strftime('%Y-%m-%d')}.log"

    root_logger = logging.getLogger("students_performance")
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s %(asctime)s: %(name)s - %(message)s")

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    _configure_root_logger()
    return logging.getLogger(name)
