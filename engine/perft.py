"""Perft tool for testing move generation correctness."""

from __future__ import annotations

import argparse
import time

from .board import Board


def perft(board: Board, depth: int) -> int:
    if depth == 0:
        return 1
    nodes = 0
    for move in board.generate_moves():
        board.push(move)
        nodes += perft(board, depth - 1)
        board.pop()
    return nodes


def bench(depth: int = 4) -> None:
    positions = {
        "startpos": ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [20, 400, 8902, 197281]),
        "kiwipete": ("r3k2r/p1ppqpb1/bn2pnp1/2PpP3/1p2P3/2N2N2/PPQ1BPPP/R3K2R w KQkq - 0 1", [48, 2039, 97862, 4085603]),
    }
    for name, (fen, expected) in positions.items():
        b = Board(fen)
        print(f"Position {name}")
        for d in range(1, depth + 1):
            t0 = time.time()
            n = perft(b, d)
            dt = time.time() - t0
            exp = expected[d - 1] if d - 1 < len(expected) else "?"
            print(f"  depth {d}: {n} nodes ({n/dt:.0f} nps) expected {exp}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("depth", type=int, nargs="?", default=4, help="search depth")
    args = parser.parse_args()
    bench(args.depth)


if __name__ == "__main__":
    main()
