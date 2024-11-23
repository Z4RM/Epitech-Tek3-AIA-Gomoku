from random import randrange
from src.Config.Config import Config
from src.Log.Logger import Logger
from src.Enums.Cell import Cell
from src.Enums.Direction import Direction
from src.Bot.Information import Information


class Bot:
    def __init__(self, config: Config, logger: Logger):
        self.information = Information(config)
        self.logger = logger
        self.map = None
        from src.Commands.Commands import Commands  # Deferred import to avoid circular dependencies issues between Bot and Commands
        self.commands = Commands(self, logger)
        self.logger.info(self.information())

    @staticmethod
    def get_weight(enemy_alignment, personal_alignment):
        return_value = 0
        match enemy_alignment:
            case 0:
                return_value += 0
            case 1:
                return_value += 1
            case 2:
                return_value += 10
            case 3:
                return_value += 100
            case 4:
                return_value += 1000
        match personal_alignment:
            case 0:
                return_value += 0
            case 1:
                return_value += 2
            case 2:
                return_value += 20
            case 3:
                return_value += 200
            case 4:
                return_value += 2000
        return return_value

    def get_best_move(self, weights_map):
        best_x = -1
        best_y = -1
        best_weight = 0

        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == Cell.Empty:
                    current_weight = weights_map[y][x]
                    if current_weight > best_weight:
                        best_weight = current_weight
                        best_x = x
                        best_y = y
        if best_x == -1 and best_y == -1:
            if self.map[len(self.map) // 2][len(self.map[0]) // 2] == Cell.Empty:
                best_y = len(self.map) // 2
                best_x = len(self.map[0]) // 2
            else:
                best_y, best_x = self.randomize_play()
        return best_y, best_x

    def check_direction(self, x, y, direction, is_personal):
        alignment = 0
        x_direction = direction.value[1]
        y_direction = direction.value[0]
        x_position = x + x_direction
        y_position = y + y_direction
        looped = 1
        while 0 <= y_position < len(self.map) < y + 5 and 0 <= x_position < x + 5 < len(self.map[y_position]):
            if self.map[y_position][x_position] == Cell.Me and is_personal:
                alignment += 1 * looped
            elif self.map[y_position][x_position] == Cell.Opponent and not is_personal:
                alignment += 1 * looped
            x_position += x_direction
            y_position += y_direction
            looped += 1
        return alignment

    def check_all_direction(self, x, y, is_personal):
        alignment = 0
        for direction in Direction:
            alignment += self.check_direction(x, y, direction, is_personal)
        return alignment

    def calc_weight(self):
        weights_map = [[Cell.Empty.value for _ in range(len(self.map[y]))] for y in range(len(self.map))]
        enemy_alignment = 0
        personal_alignment = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                weight = 0
                if self.map[y][x] == Cell.Me:
                    enemy_alignment = 0
                    personal_alignment += 1
                elif self.map[y][x] == Cell.Opponent:
                    enemy_alignment += 1
                    personal_alignment = 0
                else:
                    weight = self.get_weight(enemy_alignment, personal_alignment) + self.check_all_direction(x, y, True)
                    enemy_alignment = 0
                    personal_alignment = 0
                weights_map[y][x] = weight
        return self.get_best_move(weights_map)

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

    def randomize_play(self):
        x = randrange(len(self.map[0]))
        y = randrange(len(self.map))
        while self.map[y][x] != Cell.Empty:
            x = randrange(len(self.map[0]))
            y = randrange(len(self.map))
        return y, x

    def play(self):
        play_y, play_x = self.calc_weight()
        self.logger.debug(f"Playing at {play_x}, {play_y}")
        self.logger.debug(f"{self.information.name} is playing")
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
