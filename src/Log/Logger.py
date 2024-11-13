from datetime import datetime
from src.Config.Config import Config


LOG_LEVEL = {
    "Debug": 0,
    "Info": 1,
    "Warn": 2,
    "Error": 3,
    "Fatal": 4,
    "None": 5,
}


class Logger:
    def __init__(self, config: Config):
        try:
            self.log_level = config.get("log", "level")
        except KeyError:
            self.log_level = "None"
        if self.log_level not in LOG_LEVEL:
            self.log_level = "None"
        if self.log_level == "None":
            return
        try:
            log_file = config.get("log", "file")
        except KeyError:
            log_file = "log.txt"
        self.log_file = open(log_file, "a")
        self.log_file.write("====================\n")

    def __del__(self):
        if self.log_level != "None":
            self.log_file.close()

    def log(self, log_level, message):
        if LOG_LEVEL[self.log_level] <= LOG_LEVEL[log_level]:
            self.log_file.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {log_level}: {message}\n")
            self.log_file.flush()

    def debug(self, message):
        self.log("Debug", message)

    def info(self, message):
        self.log("Info", message)

    def warn(self, message):
        self.log("Warn", message)

    def error(self, message):
        self.log("Error", message)

    def fatal(self, message):
        self.log("Fatal", message)
