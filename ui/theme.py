"""Color theme definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Color = Tuple[int, int, int]


@dataclass
class Theme:
    light: Color
    dark: Color
    bg: Color
    highlight: Color


THEMES = {
    "classic": Theme((240, 217, 181), (181, 136, 99), (50, 50, 50), (180, 180, 0)),
    "blue": Theme((235, 235, 255), (90, 120, 160), (40, 40, 60), (255, 200, 0)),
}
