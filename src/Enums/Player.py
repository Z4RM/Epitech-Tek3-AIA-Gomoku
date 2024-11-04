from enum import Enum


class Player(Enum):
    Undefined = 0
    Player1 = 1
    Player2 = 2

    def opponent(self):
        match self:
            case Player.Player1:
                return Player.Player2
            case Player.Player2:
                return Player.Player1
            case _:
                raise ValueError("Invalid player")
