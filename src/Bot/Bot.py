from random import randrange
from src.Config.Config import Config
from src.Log.Logger import Logger
from src.Enums.Player import Player
from src.Enums.Cell import Cell
from src.Bot.Information import Information


class Bot:
    def __init__(self, config: Config, logger: Logger):
        self.information = Information(config)
        self.logger = logger
        self.map = None
        self.player = Player.Undefined
        from src.Commands.Commands import Commands  # Deferred import to avoid circular dependencies issues between Bot and Commands
        self.commands = Commands(self, logger)
        self.logger.info(self.information())

    def minimax(self, depth, alpha, beta, maximizing_player):
        #Put here the function of Mathis
            return 0

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

    def reset_map(self, width=None, height=None):
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
        self.logger.debug(f"{self.information.name} is playing")
        x = randrange(len(self.map[0]))
        y = randrange(len(self.map))
        while self.map[y][x] != Cell.Empty:
            x = randrange(len(self.map[0]))
            y = randrange(len(self.map))
        self.map[y][x] = self.player
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
