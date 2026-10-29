import logging
import os
import sys


def setup_logging() -> None:
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        stream=sys.stdout,
        force=True,
    )

    # Library loggers expose raw connection details; only show them when debugging.
    lib_level = logging.DEBUG if level <= logging.DEBUG else logging.WARNING
    for name in ("urllib3", "cloudscraper", "werkzeug"):
        logging.getLogger(name).setLevel(lib_level if name != "werkzeug" else logging.WARNING)
