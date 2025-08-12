import unittest

from engine.board import Board
from engine.perft import perft


class PerftTest(unittest.TestCase):
    def test_startpos(self):
        b = Board()
        self.assertEqual(perft(b, 1), 20)
        self.assertEqual(perft(b, 2), 400)
        self.assertEqual(perft(b, 3), 8902)

    def test_kiwipete(self):
        fen = "r3k2r/p1ppqpb1/bn2pnp1/2PpP3/1p2P3/2N2N2/PPQ1BPPP/R3K2R w KQkq - 0 1"
        b = Board(fen)
        self.assertEqual(perft(b, 1), 44)
        self.assertEqual(perft(b, 2), 1820)


if __name__ == "__main__":
    unittest.main()
