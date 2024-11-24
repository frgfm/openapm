# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.


import logging
import os
from pathlib import Path

from setuptools import setup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PKG_NAME = "openapm"
VERSION = os.getenv("BUILD_VERSION", "0.1.0.dev0")


if __name__ == "__main__":
    logger.info(f"Building wheel {PKG_NAME}-{VERSION}")

    # Dynamically set the __version__ attribute
    cwd = Path(__file__).parent.absolute()
    with cwd.joinpath(PKG_NAME, "version.py").open("w", encoding="utf-8") as f:
        f.write(f"__version__ = '{VERSION}'\n")

    setup(name=PKG_NAME, version=VERSION)
