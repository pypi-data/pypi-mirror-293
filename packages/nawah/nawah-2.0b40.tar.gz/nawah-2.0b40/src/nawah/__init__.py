"""Nawah is rapid app development framework"""

import logging
import os

logger = logging.getLogger("nawah")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)

__version__ = "2.0.b40"
