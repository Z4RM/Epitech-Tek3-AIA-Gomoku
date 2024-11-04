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

    def play(self):
        x = randrange(len(self.map))
        y = randrange(len(self.map))
        while self.map[y][x] != Cell.Empty:
            x = randrange(len(self.map))
            y = randrange(len(self.map))
        self.map[y][x] = self.player
        print(f"{x},{y}\r")

    def run(self):
        while True:
            try:
                command = input()
            except EOFError:
                break
            if self.commands.execute(command.strip()):
                break
