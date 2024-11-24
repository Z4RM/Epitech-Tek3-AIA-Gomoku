from src.Config.Config import Config
from src.Log.Logger import Logger
from src.Bot.AI import AI
from src.Enums.Cell import Cell
from src.Bot.Information import Information


class Bot:
    def __init__(self, config: Config, logger: Logger):
        self.information = Information(config)
        self.logger = logger
        self.map = None
        from src.Commands.Commands import Commands  # Deferred import to avoid circular dependencies issues between Bot and Commands
        self.commands = Commands(self, logger)
        self.logger.info(self.information())

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
        play_x, play_y = AI.get_best_move(self.map)
        self.logger.debug(f"{self.information.name} is playing at {play_x},{play_y}")
        self.map[play_y][play_x] = Cell.Me
        print(f"{play_x},{play_y}\r", flush=True)

    def run(self):
        self.logger.info(f"{self.information.name} is running")
        while True:
            try:
                command = input().strip()
            except EOFError:
                self.logger.debug("Received EOF (Ctrl + D), exiting")
                break
            except UnicodeDecodeError as error:
                # `input()` may raise an `UnicodeDecodeError` exception if (for example) "à⌫" ("⌫" = backspace) is entered
                self.commands.error(error)
                continue
            self.logger.debug(f"Received command: {command}")
            if self.commands.execute(command):
                break
        self.logger.info(f"{self.information.name} is stopping")
