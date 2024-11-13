from enum import Enum
from src.Enums.Player import Player


class Cell(Enum):
    Empty = 0
    Player1 = Player.Player1
    Player2 = Player.Player2

    @staticmethod
    def from_int(value: int) -> "Cell":
        if value == 0:
            return Cell.Empty
        if value == 1:
            return Cell.Player1
        if value == 2:
            return Cell.Player2
        raise ValueError(f"{value} is not a valid Cell")
