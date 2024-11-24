from copy import deepcopy
from random import randrange
from src.Enums.Cell import Cell

LONGEST = [
    [],                        # Cell.Empty    (unused, only set so longest[<Cell>] can be used)
    [(-1, -1), (-1, -1), -1],  # Cell.Me       [<start>, <end>, <length>]
    [(-1, -1), (-1, -1), -1]   # Cell.Opponent [<start>, <end>, <length>]
]


class AI:
    @staticmethod
    def __previous_empty(board, cell, change_x, change_y):
        cell_x = cell[0] - change_x
        cell_y = cell[1] - change_y
        return cell_x >= 0 and cell_y >= 0 and board[cell_y][cell_x] == Cell.Empty

    @staticmethod
    def __next_empty(board, cell, change_x, change_y):
        cell_x = cell[0] + change_x
        cell_y = cell[1] + change_y
        return cell_x < len(board[0]) and cell_y < len(board) and board[cell_y][cell_x] == Cell.Empty

    @staticmethod
    def __find_empty_cells_next_to_line(board, line, change_x, change_y):
        result = []
        cell_x = line[0][0] - change_x
        cell_y = line[0][1] - change_y
        if cell_x >= 0 and cell_y >= 0 and line[2] != -1 and AI.__previous_empty(board, line[0], change_x, change_y):
            result.append(((cell_x, cell_y), line[2] + 1))
        cell_x = line[1][0] + change_x
        cell_y = line[1][1] + change_y
        if cell_x >= 0 and cell_y >= 0 and line[2] != -1 and AI.__next_empty(board, line[1], change_x, change_y):
            result.append(((cell_x, cell_y), line[2] + 1))
        return result

    @staticmethod
    def __get_longest_horizontal_line(board):
        height = len(board)
        width = len(board[0])
        longest = deepcopy(LONGEST)
        for y in range(height):
            current: Cell = Cell.Empty
            start = -1, -1
            length = 0
            for x in range(width):
                if board[y][x] != current:
                    current = board[y][x]
                    if current != Cell.Empty:
                        start = x, y
                        length = 0
                if board[y][x] == current:
                    end = x, y
                    length += 1
                    if (current != Cell.Empty and length > longest[current.value][2] and
                            (AI.__previous_empty(board, start, 1, 0) or AI.__next_empty(board, end, 1, 0))):
                        longest[current.value][0] = start
                        longest[current.value][1] = end
                        longest[current.value][2] = length
        return [
            [],
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Me.value], 1, 0),
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Opponent.value], 1, 0)
        ]

    @staticmethod
    def __get_longest_vertical_line(board):
        height = len(board)
        width = len(board[0])
        longest = deepcopy(LONGEST)
        for x in range(width):
            current: Cell = Cell.Empty
            start = -1, -1
            length = 0
            for y in range(height):
                if board[y][x] != current:
                    current = board[y][x]
                    if current != Cell.Empty:
                        start = x, y
                        length = 0
                if board[y][x] == current:
                    end = x, y
                    length += 1
                    if (current != Cell.Empty and length > longest[current.value][2] and
                            (AI.__previous_empty(board, start, 0, 1) or AI.__next_empty(board, end, 0, 1))):
                        longest[current.value][0] = start
                        longest[current.value][1] = end
                        longest[current.value][2] = length
        return [
            [],
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Me.value], 0, 1),
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Opponent.value], 0, 1)
        ]

    @staticmethod
    def __get_longest_downward_diagonal_line(board):
        height = len(board)
        width = len(board[0])
        longest = deepcopy(LONGEST)
        start_x = width - 5
        while start_x >= 0:
            current: Cell = Cell.Empty
            start = -1, -1
            length = 0
            for y in range(height):
                x = start_x + y
                if x >= width:
                    break
                if board[y][x] != current:
                    current = board[y][x]
                    if current != Cell.Empty:
                        start = x, y
                        length = 0
                if board[y][x] == current:
                    end = x, y
                    length += 1
                    if (current != Cell.Empty and length > longest[current.value][2] and
                            (AI.__previous_empty(board, start, 1, 1) or AI.__next_empty(board, end, 1, 1))):
                        longest[current.value][0] = start
                        longest[current.value][1] = end
                        longest[current.value][2] = length
            start_x -= 1
        return [
            [],
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Me.value], 1, 1),
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Opponent.value], 1, 1)
        ]

    @staticmethod
    def __get_longest_upward_diagonal_line(board):
        height = len(board)
        width = len(board[0])
        longest = deepcopy(LONGEST)
        start_x = 4
        while start_x < width:
            current: Cell = Cell.Empty
            start = -1, -1
            length = 0
            for y in range(height):
                x = start_x - y
                if x < 0:
                    break
                if board[y][x] != current:
                    current = board[y][x]
                    if current != Cell.Empty:
                        start = x, y
                        length = 0
                if board[y][x] == current:
                    end = x, y
                    length += 1
                    if (current != Cell.Empty and length > longest[current.value][2] and
                            (AI.__previous_empty(board, start, -1, 1) or AI.__next_empty(board, end, -1, 1))):
                        longest[current.value][0] = start
                        longest[current.value][1] = end
                        longest[current.value][2] = length
            start_x += 1
        return [
            [],
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Me.value], -1, 1),
            AI.__find_empty_cells_next_to_line(board, longest[Cell.Opponent.value], -1, 1)
        ]

    # TODO: optimize (only one random)
    @staticmethod
    def randomize_play(board):
        height = len(board)
        width = len(board[0])
        x = randrange(width)
        y = randrange(height)
        while board[y][x] != Cell.Empty:
            x = randrange(width)
            y = randrange(height)
        return x, y

    @staticmethod
    def get_best_move(board):
        lines = [
            AI.__get_longest_horizontal_line(board),
            AI.__get_longest_vertical_line(board),
            AI.__get_longest_downward_diagonal_line(board),
            AI.__get_longest_upward_diagonal_line(board)
        ]
        cell = [
            [],              # Cell.Empty    (unused, only set so cell[<Cell>] can be used)
            [(-1, -1), -1],  # Cell.Me       [<cell>, <length>]
            [(-1, -1), -1]   # Cell.Opponent [<cell>, <length>]
        ]
        for i in range(4):
            if len(lines[i][Cell.Me.value]) and lines[i][Cell.Me.value][0][1] > cell[Cell.Me.value][1]:
                cell[Cell.Me.value] = lines[i][Cell.Me.value][0]
            if len(lines[i][Cell.Opponent.value]) and lines[i][Cell.Opponent.value][0][1] > cell[Cell.Opponent.value][1]:
                cell[Cell.Opponent.value] = lines[i][Cell.Opponent.value][0]
        if cell[Cell.Opponent.value][1] > 1 and cell[Cell.Opponent.value][1] > cell[Cell.Me.value][1]:
            return cell[Cell.Opponent.value][0]
        if cell[Cell.Me.value][1] > 1:
            return cell[Cell.Me.value][0]
        return AI.randomize_play(board)
