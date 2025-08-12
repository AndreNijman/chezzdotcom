"""Board representation and move handling for chess using a 0x88 board."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from . import fen
from .movegen import Move, generate_legal_moves

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@dataclass
class State:
    move: Move
    captured: str
    castling: int
    ep: Optional[int]
    halfmove: int
    fullmove: int


class Board:
    """Full chess board with move stack."""

    def __init__(self, start_fen: str = START_FEN) -> None:
        self.board = [" "] * 128
        self.side = 0  # 0 white, 1 black
        self.castling = 0  # bit flags KQkq -> 1 2 4 8
        self.ep: Optional[int] = None
        self.halfmove = 0
        self.fullmove = 1
        self.stack: List[State] = []
        self.set_fen(start_fen)

    # ------------------------------------------------------------------ FEN ---
    def set_fen(self, text: str) -> None:
        data = fen.parse_fen(text)
        self.board = data["board"][:]
        self.side = data["turn"]
        self.castling = data["castling"]
        self.ep = data["ep"]
        self.halfmove = data["halfmove"]
        self.fullmove = data["fullmove"]
        self.stack.clear()

    def get_fen(self) -> str:
        return fen.format_fen(self)

    # ----------------------------------------------------------- Move helpers ---
    def generate_moves(self) -> List[Move]:
        return generate_legal_moves(self)

    # ------------------------------------------------------------------ Moves ---
    def push(self, move: Move) -> None:
        captured = self.board[move.to_sq]
        state = State(move, captured, self.castling, self.ep, self.halfmove, self.fullmove)
        self.stack.append(state)

        piece = self.board[move.from_sq]
        self.board[move.from_sq] = "."
        self.board[move.to_sq] = move.promotion or piece

        self.halfmove += 1
        if captured != "." or piece.lower() == "p":
            self.halfmove = 0

        if move.flags & Move.EN_PASSANT:
            ep_sq = move.to_sq - 16 if piece.isupper() else move.to_sq + 16
            self.board[ep_sq] = "."

        self.ep = None
        if piece.lower() == "p" and abs(move.to_sq - move.from_sq) == 32:
            self.ep = (move.from_sq + move.to_sq) // 2

        if move.flags & Move.CASTLE:
            if move.to_sq == 6:  # white king side
                self.board[5] = self.board[7]
                self.board[7] = "."
            elif move.to_sq == 2:  # white queen side
                self.board[3] = self.board[0]
                self.board[0] = "."
            elif move.to_sq == 118:  # black king side
                self.board[117] = self.board[119]
                self.board[119] = "."
            elif move.to_sq == 114:  # black queen side
                self.board[115] = self.board[112]
                self.board[112] = "."

        if piece == "K":
            self.castling &= ~3
        elif piece == "k":
            self.castling &= ~12
        if move.from_sq == 0:
            self.castling &= ~2
        elif move.from_sq == 7:
            self.castling &= ~1
        elif move.from_sq == 112:
            self.castling &= ~8
        elif move.from_sq == 119:
            self.castling &= ~4
        if move.to_sq == 0:
            self.castling &= ~2
        elif move.to_sq == 7:
            self.castling &= ~1
        elif move.to_sq == 112:
            self.castling &= ~8
        elif move.to_sq == 119:
            self.castling &= ~4

        self.side ^= 1
        if self.side == 0:
            self.fullmove += 1

    def pop(self) -> None:
        state = self.stack.pop()
        move = state.move
        self.castling = state.castling
        self.ep = state.ep
        self.halfmove = state.halfmove
        self.fullmove = state.fullmove
        self.side ^= 1

        piece = self.board[move.to_sq]
        self.board[move.from_sq] = move.piece
        self.board[move.to_sq] = state.captured

        if move.flags & Move.EN_PASSANT:
            ep_sq = move.to_sq - 16 if self.side == 1 else move.to_sq + 16
            self.board[ep_sq] = "p" if self.side == 0 else "P"

        if move.flags & Move.CASTLE:
            if move.to_sq == 6:
                self.board[7] = self.board[5]
                self.board[5] = "."
            elif move.to_sq == 2:
                self.board[0] = self.board[3]
                self.board[3] = "."
            elif move.to_sq == 118:
                self.board[119] = self.board[117]
                self.board[117] = "."
            elif move.to_sq == 114:
                self.board[112] = self.board[115]
                self.board[115] = "."

    # --------------------------------------------------------------- In-check ---
    def king_square(self, side: int) -> int:
        target = "K" if side == 0 else "k"
        for i, p in enumerate(self.board):
            if not (i & 0x88) and p == target:
                return i
        raise ValueError("King not found")

    def is_square_attacked(self, sq: int, by_side: int) -> bool:
        from .movegen import attacks_on_square
        return attacks_on_square(self, sq, by_side)

    def in_check(self, side: Optional[int] = None) -> bool:
        side = self.side if side is None else side
        ks = self.king_square(side)
        return self.is_square_attacked(ks, side ^ 1)
