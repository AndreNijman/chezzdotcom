"""Zobrist hashing utilities."""

from __future__ import annotations

import random

random.seed(2021)

PIECES = "PNBRQKpnbrqk"


def _rand64() -> int:
    return random.getrandbits(64)


piece_keys = {p: [_rand64() for _ in range(64)] for p in PIECES}
castling_keys = [_rand64() for _ in range(16)]
ep_keys = [_rand64() for _ in range(64)]
side_key = _rand64()


def hash_board(board) -> int:
    h = 0
    for sq in range(64):
        bb_sq = (sq & 7) + ((sq // 8) << 4)
        piece = board.board[bb_sq]
        if piece != ".":
            h ^= piece_keys[piece][sq]
    h ^= castling_keys[board.castling]
    if board.ep is not None:
        h ^= ep_keys[board.ep & 63]
    if board.side:
        h ^= side_key
    return h
