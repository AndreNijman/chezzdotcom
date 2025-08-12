"""Simple pygame UI widgets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple

import pygame

Color = Tuple[int, int, int]


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    callback: Callable[[], None]
    font: pygame.font.Font
    base_color: Color = (200, 200, 200)
    hover_color: Color = (255, 255, 255)

    def draw(self, surf: pygame.Surface) -> None:
        mouse = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse) else self.base_color
        pygame.draw.rect(surf, color, self.rect)
        label = self.font.render(self.text, True, (0, 0, 0))
        surf.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
