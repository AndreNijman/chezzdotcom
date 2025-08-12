"""
Sprite pack helper.

All graphics for pieces and UI icons are generated procedurally on the first run
by :mod:`assets.generate_sprites`.  This module exposes a convenience function
that ensures the images exist on disk.
"""

from __future__ import annotations

import os
from .generate_sprites import generate_all

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")


def ensure_assets() -> None:
    """Generate assets if missing."""
    if not os.path.exists(IMG_DIR) or not os.listdir(IMG_DIR):
        os.makedirs(IMG_DIR, exist_ok=True)
        generate_all(IMG_DIR)
