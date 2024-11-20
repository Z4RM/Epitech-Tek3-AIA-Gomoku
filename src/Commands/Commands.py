from src.Bot.Bot import Bot
from src.Log.Logger import Logger
from src.Enums.Player import Player
from src.Enums.Cell import Cell
from src.Commands.Command import Command
from src.Commands.CommandSuite import CommandSuite

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
            "BOARD": Command(CommandSuite(self.board_suite_iteration, "DONE", self.board_suite_end), [START_REQUIREMENT]),
            "BEGIN": Command(self.begin, [START_REQUIREMENT]),
            "INFO": Command(self.info),
            "TURN": Command(self.turn, [START_REQUIREMENT]),
            "PLAY": Command(self.play, [START_REQUIREMENT]),
            "TAKEBACK": Command(self.takeback, [START_REQUIREMENT]),
            "END": Command(self.end)
        }
        self.suite = None

    # region Command execution
    def execute(self, command):
        split_command = command.split()
        command = split_command[0]
        if len(split_command) < 1:
            self.logger.error("Received empty command")
            return
        if self.suite is not None:
            return self.suite(split_command)
        if command not in self.commands:
            self.unknown(f"Unknown command: {command}")
            return
        if not self.has_requirements(command):
            return
        self.logger.debug(f"Executing command: {command}")
        if isinstance(self.commands[command].command, CommandSuite):
            self.suite = self.commands[command].command
            return self.suite(split_command)
        return self.commands[command](split_command)

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
    # endregion

    def about(self, _):
        print(self.bot.information())

    def start(self, command):
        if len(command) <= 1:
            return self.error("Missing size in START command")
        size = int(command[1])
        if size < 5:
            return self.error(f"Invalid size in START command: {size} (too small)")
        self.bot.reset(size)
        self.bot.size = size
        print("OK\r")

    def rectstart(self, command):
        x, y = self.__get_coordinates_from_command(command, "RECTSTART")
        if x < 5:
            return self.error(f"Invalid width in RECTSTART command: {x} (too small)")
        if y < 5:
            return self.error(f"Invalid width in RECTSTART command: {y} (too small)")
        self.bot.reset(x, y)
        print("OK\r")

    def restart(self, _):
        self.bot.reset()
        print("OK\r")

    def swap2board(self, _):
        return self.unknown("SWAP2BOARD command isn't yet implemented")

    # region BOARD
    def board_suite_iteration(self, command):
        data = command[0].split(",")
        if len(data) != 3:
            return self.error(f"Invalid data: {command[0]}")
        x = int(data[0])
        y = int(data[1])
        if x >= len(self.bot.map[0]) or y >= len(self.bot.map):
            return self.error(f"Invalid coordinates: {x}, {y}")
        match data[2]:
            case "1":
                self.bot.map[y][x] = Player.Player1
            case "2":
                self.bot.map[y][x] = Player.Player2
            case _:
                return self.error(f"Invalid field: {data[2]}")

    def board_suite_end(self, _):
        self.suite = None
        self.bot.play()
    # endregion

    def begin(self, _):
        self.bot.play()

    def info(self, _):
        pass

    def turn(self, command):
        x, y = self.__get_coordinates_from_command(command, "TURN")
        if x >= len(self.bot.map[0]) or y >= len(self.bot.map):
            return self.error(f"Invalid coordinates: {x}, {y}")
        self.bot.map[y][x] = Player.Player2
        self.bot.play()

    def play(self, command):
        x, y = self.__get_coordinates_from_command(command, "PLAY")
        if x >= len(self.bot.map[0]) or y >= len(self.bot.map):
            return self.error(f"Invalid coordinates: {x}, {y}")
        self.bot.map[y][x] = Player.Player1
        print(f"{x},{y}\r")

    def takeback(self, command):
        x, y = self.__get_coordinates_from_command(command, "TAKEBACK")
        if x >= len(self.bot.map[0]) or y >= len(self.bot.map):
            return self.error(f"Invalid coordinates: {x}, {y}")
        self.bot.map[y][x] = Cell.Empty
        print("OK\r")

    @staticmethod
    def end(_):
        return True

    # region Errors
    def unknown(self, message):
        self.logger.error(message)
        print(f"UNKNOWN {message}\r")
        return False

    def error(self, message):
        self.logger.error(message)
        print(f"ERROR {message}\r")
        return False
    # endregion

    def __get_coordinates_from_command(self, command, command_name):
        if len(command) <= 1:
            return self.error(f"Missing coordinates in {command_name} command")
        coordinate = command[1].split(",")
        if len(coordinate) != 2:
            return self.error(f"Invalid coordinates in {command_name} command: {command[1]}")
        return int(coordinate[0]), int(coordinate[1])
