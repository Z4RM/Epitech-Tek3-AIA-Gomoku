from src.Bot.Bot import Bot
from src.Log.Logger import Logger
from src.Enums.Player import Player
from src.Enums.Cell import Cell
from src.Commands.Command import Command


class Commands:
    def __init__(self, bot: Bot, logger: Logger):
        self.bot = bot
        self.logger = logger
        self.commands = {
            "ABOUT": Command(self.about),
            "START": Command(self.start),
            "BEGIN": Command(self.begin, ["START"]),
            "INFO": Command(self.info),
            "BOARD": None,  # TODO
            "TURN": Command(self.turn, ["START"]),
            "END": Command(self.end)
            # TODO: other commands
        }

    def execute(self, command):
        command = command.split()
        if len(command) < 1:
            self.logger.error("Received empty command")
            return
        if command[0] not in self.commands or self.commands[command[0]] is None:
            self.logger.error(f"Unknown command: {command[0]}")
            print(f"UNKNOWN Unknown command: {command[0]}\r")
            return
        if self.commands[command[0]].requirements is not None:
            for requirement in self.commands[command[0]].requirements:
                if not self.commands[requirement].executions:
                    self.logger.error(f"Requirement not met for {command[0]}: {requirement}")
                    print(f"ERROR {requirement} must be executed before {command[0]}\r")
                    return
        self.logger.debug(f"Executing command: {command[0]}")
        return self.commands[command[0]](command)

    def about(self, _):
        print(self.bot.information())

    def start(self, command):
        if len(command) <= 1:
            return self.error("Missing size in START command")
        size = int(command[1])
        if size < 5:
            return self.error(f"Invalid size in START command: {size} (too small)")
        self.bot.map = [[Cell.Empty for _ in range(size)] for _ in range(size)]
        print("OK\r")

    def begin(self, _):
        self.bot.player = Player.Player1
        self.bot.play()

    def info(self, _):
        pass

    def turn(self, command):
        if len(command) <= 1:
            return self.error("Missing coordinates in TURN command")
        if self.bot.player == Player.Undefined:
            self.bot.player = Player.Player2
        coordinate = command[1].split(",")
        if len(coordinate) != 2:
            return self.error(f"Invalid coordinates in TURN command: {command[1]}")
        x = int(coordinate[0])
        y = int(coordinate[1])
        self.bot.map[y][x] = self.bot.player.opponent()
        self.bot.play()

    @staticmethod
    def end(_):
        return True

    def error(self, message):
        self.logger.error(message)
        print(f"ERROR {message}\r")
        return False
