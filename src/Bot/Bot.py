from random import randrange
from src.Config.Config import Config
from src.Log.Logger import Logger
from src.Enums.Player import Player
from src.Enums.Cell import Cell
from src.Enums.Direction import Direction
from src.Bot.Information import Information

class Bot:
    def __init__(self, config: Config, logger: Logger):
        self.information = Information(config)
        self.logger = logger
        self.map = None
        self.size = 0
        self.player = Player.Undefined
        from src.Commands.Commands import Commands  # Deferred import to avoid circular dependencies issues between Bot and Commands
        self.commands = Commands(self, logger)
        self.logger.info(self.information())

    def check_line(self, y, x, direction):
        dy, dx = direction
        weight = 0
        for i in range(1, 6):
            tmp_y = y + dy * i
            tmp_x = x + dx * i
            if tmp_y < 0 or tmp_x < 0 or tmp_y >= 20 or tmp_x >= 20 or (tmp_y == y and tmp_x == x):
                continue
            cell = self.map[tmp_y][tmp_x]
            if cell == self.player:
                weight += 5
            elif cell == Cell.Empty:
                weight += 0
            else:
                weight += -2
        return weight

    def check_case(self, y, x, player):
        up_left_line = self.check_line(y, x, Direction.UL.value)
        up_right_line = self.check_line(y, x, Direction.UR.value)
        up_line = self.check_line(y, x, Direction.UP.value)
        left_line = self.check_line(y, x, Direction.LEFT.value)
        right_line = self.check_line(y, x, Direction.RIGHT.value)
        down_left_line = self.check_line(y, x, Direction.DL.value)
        down_right_line = self.check_line(y, x, Direction.DR.value)
        down_line = self.check_line(y, x, Direction.DOWN.value)
        weight = up_left_line + up_right_line + up_line + left_line + right_line + down_left_line + down_right_line + down_line
        return weight

    def calc_weight(self):
        weight_map = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for cell_y in range(self.size):
            for cell_x in range(self.size):
                cell = self.map[cell_y][cell_x]
                if cell is Cell.Empty:
                    weight_map[cell_y][cell_x] = self.check_case(cell_y, cell_x, 1)
                cell = -1
        best_y = 0
        best_x = 0
        best_weight = 0
        for cy in range(self.size):
            for cx in range(self.size):
                if weight_map[cy][cy] > best_weight:
                    best_y = cy
                    best_x = cx
        return best_y, best_x

    def minimax(self, depth, alpha, beta, maximizing_player):
        return self.calc_weight()

    def evaluate_window(self, window):
        score = 0
        player1_count = window.count(Cell.Player1)
        player2_count = window.count(Cell.Player2)

        if player1_count == 5:
            score += 100000
        elif player2_count == 5:
            score -= 100000
        if player1_count == 4 and window.count(Cell.Empty) == 1:
            score += 1000
        elif player2_count == 4 and window.count(Cell.Empty) == 1:
            score -= 1000
        if player1_count == 3 and window.count(Cell.Empty) == 2:
            score += 100
        elif player2_count == 3 and window.count(Cell.Empty) == 2:
            score -= 100
        if player1_count == 2 and window.count(Cell.Empty) == 3:
            score += 10
        elif player2_count == 2 and window.count(Cell.Empty) == 3:
            score -= 10

        return score

    def evaluate(self):
        score = 0

        for row in range(len(self.map)):
            for col in range(len(self.map[0]) - 4):
                window = self.map[row][col:col + 5]
                score += self.evaluate_window(window)
        for col in range(len(self.map[0])):
            for row in range(len(self.map) - 4):
                window = [self.map[row + i][col] for i in range(5)]
                score += self.evaluate_window(window)
        for row in range(len(self.map) - 4):
            for col in range(len(self.map[0]) - 4):
                window = [self.map[row + i][col + i] for i in range(5)]
                score += self.evaluate_window(window)
        for row in range(4, len(self.map)):
            for col in range(len(self.map[0]) - 4):
                window = [self.map[row - i][col + i] for i in range(5)]
                score += self.evaluate_window(window)

        return score

    def get_possible_moves(self):
        moves = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == Cell.Empty:
                    moves.append((x, y))
        return moves

    def check_winner(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[0]) - 4):
                if self.map[row][col] != Cell.Empty and self.map[row][col] == self.map[row][col + 1] == self.map[row][
                    col + 2] == self.map[row][col + 3] == self.map[row][col + 4]:
                    return self.map[row][col]
        for col in range(len(self.map[0])):
            for row in range(len(self.map) - 4):
                if self.map[row][col] != Cell.Empty and self.map[row][col] == self.map[row + 1][col] == \
                        self.map[row + 2][col] == self.map[row + 3][col] == self.map[row + 4][col]:
                    return self.map[row][col]
        for row in range(len(self.map) - 4):
            for col in range(len(self.map[0]) - 4):
                if self.map[row][col] != Cell.Empty and self.map[row][col] == self.map[row + 1][col + 1] == \
                        self.map[row + 2][col + 2] == self.map[row + 3][col + 3] == self.map[row + 4][col + 4]:
                    return self.map[row][col]
        for row in range(4, len(self.map)):
            for col in range(len(self.map[0]) - 4):
                if self.map[row][col] != Cell.Empty and self.map[row][col] == self.map[row - 1][col + 1] == \
                        self.map[row - 2][col + 2] == self.map[row - 3][col + 3] == self.map[row - 4][col + 4]:
                    return self.map[row][col]

        return None

    def reset(self, width=None, height=None):
        if width is None:
            if self.map is not None:
                width = len(self.map[0])
            else:
                raise ValueError("Width is not provided and map is not initialized")
        if height is None:
            if self.map is not None:
                height = len(self.map)
            else:
                height = width
        self.map = [[Cell.Empty for _ in range(width)] for _ in range(height)]

    def play(self):
        play_y, play_x = self.minimax(1, 0, 0, 2)
        self.logger.debug(f"{self.information.name} is playing")
        x = randrange(len(self.map[0]))
        y = randrange(len(self.map))
        while self.map[y][x] != Cell.Empty:
            x = randrange(len(self.map[0]))
            y = randrange(len(self.map))
        self.map[play_y][play_x] = self.player
        print(f"{x},{y}\r")

    def run(self):
        self.logger.info(f"{self.information.name} is running")
        while True:
            try:
                command = input().strip()
            except EOFError:
                self.logger.debug("Received EOF (Ctrl + D), exiting")
                break
            self.logger.debug(f"Received command: {command}")
            if self.commands.execute(command):
                break
        self.logger.info(f"{self.information.name} is stopping")
