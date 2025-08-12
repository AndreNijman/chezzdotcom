"""Alpha-beta chess search with simple evaluation."""

from __future__ import annotations

import math
import time
from typing import Dict, Optional, Tuple

from engine.board import Board, Move
from engine.zobrist import hash_board

PIECE_VALUES = {
    "p": 100,
    "n": 320,
    "b": 330,
    "r": 500,
    "q": 900,
    "k": 0,
}


class Searcher:
    """Simple iterative deepening alpha-beta search."""

    def __init__(self, board: Board, max_time: float = 1.0) -> None:
        self.board = board
        self.max_time = max_time
        self.start_time: float = 0.0
        self.tt: Dict[int, Tuple[int, int, Optional[Move]]] = {}

    def evaluate(self) -> int:
        score = 0
        for sq in range(128):
            if sq & 0x88:
                continue
            p = self.board.board[sq]
            if p == ".":
                continue
            val = PIECE_VALUES[p.lower()]
            score += val if p.isupper() else -val
        return score if self.board.side == 0 else -score

    def search(self, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Move]]:
        if time.time() - self.start_time > self.max_time:
            raise TimeoutError
        key = hash_board(self.board)
        if key in self.tt and self.tt[key][0] >= depth:
            return self.tt[key][1], self.tt[key][2]
        if depth == 0:
            return self.evaluate(), None
        best_move: Optional[Move] = None
        for move in self.board.generate_moves():
            self.board.push(move)
            score, _ = self.search(depth - 1, -beta, -alpha)
            score = -score
            self.board.pop()
            if score > alpha:
                alpha, best_move = score, move
            if alpha >= beta:
                break
        self.tt[key] = (depth, alpha, best_move)
        return alpha, best_move

    def best_move(self, max_depth: int = 3) -> Move:
        self.start_time = time.time()
        best = None
        for depth in range(1, max_depth + 1):
            try:
                score, move = self.search(depth, -math.inf, math.inf)
                if move:
                    best = move
            except TimeoutError:
                break
        assert best
        return best
