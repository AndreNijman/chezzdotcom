"""Asset loading helper."""

from __future__ import annotations

import os
from typing import Dict

import pygame

from .spritepack import ensure_assets as _ensure_assets

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")


def ensure_assets() -> None:
    _ensure_assets()


def load_images() -> Dict[str, Dict[str, pygame.Surface]]:
    ensure_assets()
    pieces = {}
    for piece in "PNBRQKpnbrqk":
        img = pygame.image.load(os.path.join(IMG_DIR, f"{piece}64.png")).convert_alpha()
        pieces[piece] = img
    icons = {}
    for name in ("undo", "redo", "save", "load", "settings", "play", "pause", "flip", "theme", "new", "quit"):
        icons[name] = pygame.image.load(os.path.join(IMG_DIR, f"{name}.png")).convert_alpha()
    return {"pieces": pieces, "icons": icons}
