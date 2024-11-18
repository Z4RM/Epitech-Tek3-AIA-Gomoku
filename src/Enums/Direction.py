from enum import Enum


class Direction(Enum):
    UL = [-1, -1]   #   ↖
    UP = [-1, 0]    #   ↑
    UR = [-1, 1]    #   ↗
    LEFT = [0, -1]  #   ←
    RIGHT = [0, 1]  #   →
    DL = [1, -1]    #   ↙
    DOWN = [1, 0]   #   ↓
    DR = [1, 1]     #   ↘

    def __getitem__(self, key):
        return getattr(self, key)