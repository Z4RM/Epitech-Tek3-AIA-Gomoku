from src.Config.Config import Config
from src.Log.Logger import Logger
from src.Bot.Bot import Bot


def main():
    config = Config()
    logger = Logger(config)
    bot = Bot(config, logger)
    bot.run()


if __name__ == "__main__":
    main()
