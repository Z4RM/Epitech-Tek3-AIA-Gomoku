from src.Bot.Bot import Bot
from src.Log.Logger import Logger
from src.Enums.Player import Player
from src.Enums.Cell import Cell
from src.Commands.Command import Command

START_REQUIREMENT = ["START", "RECTSTART"]


class Commands:
    def __init__(self, bot: Bot, logger: Logger):
        self.bot = bot
        self.logger = logger
        self.commands = {
            "ABOUT": Command(self.about),
            "START": Command(self.start),
            "RECTSTART": Command(self.rectstart),
            "RESTART": Command(self.restart, [START_REQUIREMENT]),
            "SWAP2BOARD": Command(self.swap2board, [START_REQUIREMENT]),
            "BOARD": Command(self.board, [START_REQUIREMENT]),
            "BEGIN": Command(self.begin, [START_REQUIREMENT]),
            "INFO": Command(self.info),
            "TURN": Command(self.turn, [START_REQUIREMENT]),
            "PLAY": Command(self.play, [START_REQUIREMENT]),
            "TAKEBACK": Command(self.takeback, [START_REQUIREMENT]),
            "END": Command(self.end)
        }

    def execute(self, command):
        command = command.split()
        if len(command) < 1:
            self.logger.error("Received empty command")
            return
        if command[0] not in self.commands:
            self.unknown(f"Unknown command: {command[0]}")
            return
        if not self.has_requirements(command[0]):
            return
        self.logger.debug(f"Executing command: {command[0]}")
        return self.commands[command[0]](command)

    def has_requirements(self, command):
        if self.commands[command].requirements is None:
            return True
        for requirement in self.commands[command].requirements:
            if isinstance(requirement, list):
                executed = 0
                for r in requirement:
                    if self.commands[r].executions:
                        executed += 1
                if executed == 0:
                    print(f"One of these commands must be executed before {command}: {', '.join(requirement)}\r")
                    return False
            elif not self.commands[requirement].executions:
                print(f"{requirement} command must be executed before {command}\r")
                return False
        return True

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

    def rectstart(self, _):
        return self.unknown("RECTSTART command isn't yet implemented")

    def restart(self, _):
        return self.unknown("RESTART command isn't yet implemented")

    def swap2board(self, _):
        return self.unknown("SWAP2BOARD command isn't yet implemented")

    def board(self, _):
        return self.unknown("BOARD command isn't yet implemented")

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

    def play(self, _):
        return self.unknown("PLAY command isn't yet implemented")

    def takeback(self, _):
        return self.unknown("TAKEBACK command isn't yet implemented")

    @staticmethod
    def end(_):
        return True

    def unknown(self, message):
        self.logger.error(message)
        print(f"UNKNOWN {message}\r")
        return False

    def error(self, message):
        self.logger.error(message)
        print(f"ERROR {message}\r")
        return False
