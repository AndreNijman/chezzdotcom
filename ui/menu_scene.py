"""Main menu scene with simple buttons."""

from __future__ import annotations

import pygame

from ui.widgets import Button


class MenuScene:
    def __init__(self, app) -> None:
        self.app = app
        self.font = pygame.font.SysFont("arial", 32)
        width, height = self.app.screen.get_size()
        btn_w, btn_h = 200, 60
        cx, cy = width // 2 - btn_w // 2, height // 2 - btn_h // 2
        self.buttons = [
            Button(pygame.Rect(cx, cy - 70, btn_w, btn_h), "Play", self.start_game, self.font),
            Button(pygame.Rect(cx, cy + 10, btn_w, btn_h), "Quit", self.quit_game, self.font),
        ]

    def start_game(self) -> None:
        from ui.game_scene import GameScene
        self.next_scene = GameScene(self.app)

    def quit_game(self) -> None:
        self.next_scene = None

    def run(self):
        self.next_scene = self
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                return None
            for b in self.buttons:
                b.handle_event(event)
        self.app.screen.fill((40, 40, 40))
        for b in self.buttons:
            b.draw(self.app.screen)
        pygame.display.flip()
        return self.next_scene
