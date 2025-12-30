import logging

from .config import config


def setup_logging() -> None:
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
