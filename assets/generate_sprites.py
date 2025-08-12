"""Procedurally draw piece sprites and UI icons using pygame."""

from __future__ import annotations

import os
from typing import Dict

import pygame

PIECES = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}

ICONS = {
    "undo": "↶",
    "redo": "↷",
    "save": "💾",
    "load": "📂",
    "settings": "⚙",
    "play": "▶",
    "pause": "⏸",
    "flip": "🔁",
    "theme": "🎨",
    "new": "★",
    "quit": "✖",
}


def render_text(symbol: str, size: int, color=(0, 0, 0)) -> pygame.Surface:
    font = pygame.font.SysFont("dejavusans", size)
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    text = font.render(symbol, True, color)
    rect = text.get_rect(center=(size // 2, size // 2))
    surf.blit(text, rect)
    return surf


def generate_all(path: str) -> Dict[str, pygame.Surface]:
    pygame.init()
    os.makedirs(path, exist_ok=True)
    for piece, symbol in PIECES.items():
        for size in (128, 64):
            surf = render_text(symbol, size, (0, 0, 0) if piece.islower() else (255, 255, 255))
            pygame.image.save(surf, os.path.join(path, f"{piece}{size}.png"))
    for name, symbol in ICONS.items():
        surf = render_text(symbol, 64, (0, 0, 0))
        pygame.image.save(surf, os.path.join(path, f"{name}.png"))
    pygame.quit()
    return {}
