from enum import Enum


class Direction(Enum):
    UL = [-1, -1, 'UP LEFT']   #   ↖
    UP = [-1, 0, 'UP']    #   ↑
    UR = [-1, 1, 'UP RIGHT']    #   ↗
    LEFT = [0, -1, 'LEFT']  #   ←
    RIGHT = [0, 1, 'RIGHT']  #   →
    DL = [1, -1, 'DOWN LEFT']    #   ↙
    DOWN = [1, 0, 'DOWN']   #   ↓
    DR = [1, 1, 'DOWN RIGHT']     #   ↘

    def __getitem__(self, key):
        return getattr(self, key)