"""
README
======

A lightweight chess program built with ``pygame``.  The goal of this project is
 to provide a compact yet fully playable chess implementation with a minimal AI
 and a simple user interface.

Running
-------

.. code-block:: console

    $ python main.py

Controls
--------

- Mouse    : click or drag pieces to make moves
- N        : new game
- U / R    : undo / redo
- S / L    : save / load (JSON file)
- F        : flip board
- P        : toggle pause menu
- Q / ESC  : quit

The game generates its own sprites on first start and stores them in
``assets/images``.  Everything runs fully offline.

"""

import pygame
from assets.asset_loader import ensure_assets, load_images
from ui.menu_scene import MenuScene


class Game:
    """Application controller."""

    def __init__(self) -> None:
        pygame.init()
        ensure_assets()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Pygame Chess")
        self.clock = pygame.time.Clock()
        self.images = load_images()
        self.scene = MenuScene(self)

    def run(self) -> None:
        """Main loop dispatching to active scene."""
        while self.scene:
            self.clock.tick(60)
            self.scene = self.scene.run()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
