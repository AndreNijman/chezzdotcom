"""Legal move generation using 0x88 board coordinates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, List, Optional

KNIGHT_DIRS = [31, 33, 14, -14, 18, -18, -31, -33]
BISHOP_DIRS = [15, 17, -15, -17]
ROOK_DIRS = [16, -16, 1, -1]
KING_DIRS = BISHOP_DIRS + ROOK_DIRS


@dataclass
class Move:
    from_sq: int
    to_sq: int
    piece: str
    promotion: Optional[str] = None
    flags: int = 0

    CAPTURE = 1 << 0
    EN_PASSANT = 1 << 1
    CASTLE = 1 << 2
    PROMOTION = 1 << 3


def generate_pseudo_moves(board, include_castling: bool = True) -> Generator[Move, None, None]:
    """Yield pseudo legal moves."""
    side = board.side
    for sq in range(128):
        if sq & 0x88:
            continue
        piece = board.board[sq]
        if piece == "." or (piece.isupper() != (side == 0)):
            continue
        if piece.lower() == "p":
            direction = 16 if piece.isupper() else -16
            start_rank = 1 if piece.isupper() else 6
            promotion_rank = 7 if piece.isupper() else 0
            to = sq + direction
            if not (to & 0x88) and board.board[to] == ".":
                if (to >> 4) == promotion_rank:
                    for prom in "QRBN":
                        yield Move(sq, to, piece, prom if piece.isupper() else prom.lower(), Move.PROMOTION)
                else:
                    yield Move(sq, to, piece)
                to2 = to + direction
                if (sq >> 4) == start_rank and board.board[to2] == ".":
                    yield Move(sq, to2, piece)
            for cap_dir in (15, 17) if piece.isupper() else (-15, -17):
                to = sq + cap_dir
                if to & 0x88:
                    continue
                target = board.board[to]
                if target != "." and target.isupper() != piece.isupper():
                    if (to >> 4) == promotion_rank:
                        for prom in "QRBN":
                            yield Move(sq, to, piece, prom if piece.isupper() else prom.lower(), Move.CAPTURE | Move.PROMOTION)
                    else:
                        yield Move(sq, to, piece, None, Move.CAPTURE)
                if board.ep is not None and to == board.ep:
                    yield Move(sq, to, piece, None, Move.EN_PASSANT | Move.CAPTURE)
        elif piece.lower() == "n":
            for d in KNIGHT_DIRS:
                to = sq + d
                if to & 0x88:
                    continue
                target = board.board[to]
                if target == "." or target.isupper() != piece.isupper():
                    flags = Move.CAPTURE if target != "." else 0
                    yield Move(sq, to, piece, None, flags)
        elif piece.lower() in ("b", "r", "q"):
            dirs = BISHOP_DIRS if piece.lower() == "b" else ROOK_DIRS if piece.lower() == "r" else KING_DIRS
            for d in dirs:
                to = sq + d
                while not (to & 0x88):
                    target = board.board[to]
                    if target == ".":
                        yield Move(sq, to, piece)
                    else:
                        if target.isupper() != piece.isupper():
                            yield Move(sq, to, piece, None, Move.CAPTURE)
                        break
                    to += d
        elif piece.lower() == "k":
            for d in KING_DIRS:
                to = sq + d
                if to & 0x88:
                    continue
                target = board.board[to]
                if target == "." or target.isupper() != piece.isupper():
                    flags = Move.CAPTURE if target != "." else 0
                    yield Move(sq, to, piece, None, flags)
            if include_castling:
                if piece == "K":
                    if board.castling & 1 and board.board[5] == board.board[6] == "." and not board.in_check(0) and not board.is_square_attacked(5, 1) and not board.is_square_attacked(6, 1):
                        yield Move(4, 6, piece, None, Move.CASTLE)
                    if board.castling & 2 and board.board[1] == board.board[2] == board.board[3] == "." and not board.in_check(0) and not board.is_square_attacked(3, 1) and not board.is_square_attacked(2, 1):
                        yield Move(4, 2, piece, None, Move.CASTLE)
                elif piece == "k":
                    if board.castling & 4 and board.board[117] == board.board[118] == "." and not board.in_check(1) and not board.is_square_attacked(117, 0) and not board.is_square_attacked(118, 0):
                        yield Move(116, 118, piece, None, Move.CASTLE)
                    if board.castling & 8 and board.board[113] == board.board[114] == board.board[115] == "." and not board.in_check(1) and not board.is_square_attacked(115, 0) and not board.is_square_attacked(114, 0):
                        yield Move(116, 114, piece, None, Move.CASTLE)


def attacks_on_square(board, sq: int, by_side: int) -> bool:
    orig_side = board.side
    board.side = by_side
    for move in generate_pseudo_moves(board, include_castling=False):
        if move.to_sq == sq:
            board.side = orig_side
            return True
    board.side = orig_side
    return False


def generate_legal_moves(board) -> List[Move]:
    res: List[Move] = []
    for move in generate_pseudo_moves(board):
        board.push(move)
        if not board.in_check(board.side ^ 1):
            res.append(move)
        board.pop()
    return res
