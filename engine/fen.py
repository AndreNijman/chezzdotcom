"""Parsing and writing Forsyth–Edwards Notation (FEN)."""

from __future__ import annotations

from typing import Dict, Optional


def parse_fen(text: str) -> Dict:
    fields = text.strip().split()
    board_field, turn, castling, ep, halfmove, fullmove = fields
    board = [" "] * 128
    for sq in range(128):
        if not (sq & 0x88):
            board[sq] = "."
    ranks = board_field.split("/")
    for r, rank in enumerate(ranks):
        file = 0
        for ch in rank:
            if ch.isdigit():
                file += int(ch)
            else:
                sq = (7 - r) * 16 + file
                board[sq] = ch
                file += 1
    turn_val = 0 if turn == "w" else 1
    castling_val = 0
    if "K" in castling:
        castling_val |= 1
    if "Q" in castling:
        castling_val |= 2
    if "k" in castling:
        castling_val |= 4
    if "q" in castling:
        castling_val |= 8
    ep_sq: Optional[int] = None
    if ep != "-":
        file = ord(ep[0]) - ord("a")
        rank = int(ep[1]) - 1
        ep_sq = rank * 16 + file
    return {
        "board": board,
        "turn": turn_val,
        "castling": castling_val,
        "ep": ep_sq,
        "halfmove": int(halfmove),
        "fullmove": int(fullmove),
    }


def format_fen(board) -> str:
    pieces = []
    for r in range(7, -1, -1):
        empty = 0
        rank = ""
        for f in range(8):
            sq = r * 16 + f
            piece = board.board[sq]
            if piece == ".":
                empty += 1
            else:
                if empty:
                    rank += str(empty)
                    empty = 0
                rank += piece
        if empty:
            rank += str(empty)
        pieces.append(rank)
    board_field = "/".join(pieces)
    turn = "w" if board.side == 0 else "b"
    castling = ""
    if board.castling & 1:
        castling += "K"
    if board.castling & 2:
        castling += "Q"
    if board.castling & 4:
        castling += "k"
    if board.castling & 8:
        castling += "q"
    castling = castling or "-"
    ep = "-"
    if board.ep is not None:
        file = chr(ord("a") + (board.ep & 7))
        rank = str((board.ep >> 4) + 1)
        ep = file + rank
    return f"{board_field} {turn} {castling} {ep} {board.halfmove} {board.fullmove}"
