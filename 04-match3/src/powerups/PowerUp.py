from src.Tile import Tile
from src.Board import Board

class PowerUp(Tile):
    def __init__(self, i: int, j: int, color: int, variety: int):
        super().__init__(i, j, color, variety)
        self.is_powerup = True

    def activate(self, board: Board) -> set:
        return set()