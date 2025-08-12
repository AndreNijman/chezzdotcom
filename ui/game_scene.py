"""Main in-game scene handling rendering and input."""

from __future__ import annotations

from typing import Optional, Tuple

import pygame

from ai.search import Searcher
from engine.board import Board, Move
from ui.theme import THEMES

Square = Tuple[int, int]


class GameScene:
    def __init__(self, app) -> None:
        self.app = app
        self.board = Board()
        self.images = app.images
        self.theme = THEMES["classic"]
        self.selected: Optional[int] = None
        self.searcher: Optional[Searcher] = None

    def draw_board(self, surf: pygame.Surface) -> None:
        sq_size = 64
        for rank in range(8):
            for file in range(8):
                sq = rank * 16 + file
                color = self.theme.light if (rank + file) % 2 == 0 else self.theme.dark
                r = pygame.Rect(file * sq_size, (7 - rank) * sq_size, sq_size, sq_size)
                pygame.draw.rect(surf, color, r)
                piece = self.board.board[sq]
                if piece != ".":
                    img = self.images["pieces"][piece]
                    surf.blit(img, r)

    def handle_event(self, event: pygame.event.Event) -> Optional["GameScene"]:
        if event.type == pygame.QUIT:
            return None
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from ui.menu_scene import MenuScene
            return MenuScene(self.app)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            file = event.pos[0] // 64
            rank = 7 - event.pos[1] // 64
            sq = rank * 16 + file
            if self.selected is None:
                piece = self.board.board[sq]
                if piece == "." or (piece.isupper() != (self.board.side == 0)):
                    return self
                self.selected = sq
            else:
                move = self.find_move(self.selected, sq)
                self.selected = None
                if move:
                    self.board.push(move)
                    if self.board.generate_moves():
                        self.searcher = Searcher(self.board)
                        reply = self.searcher.best_move()
                        self.board.push(reply)
        return self

    def find_move(self, from_sq: int, to_sq: int) -> Optional[Move]:
        for m in self.board.generate_moves():
            if m.from_sq == from_sq and m.to_sq == to_sq:
                return m
        return None

    def run(self) -> Optional["GameScene"]:
        for event in pygame.event.get():
            scene = self.handle_event(event)
            if scene is not self:
                return scene
        self.draw_board(self.app.screen)
        pygame.display.flip()
        return self
