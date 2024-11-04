from src.Config.Config import Config


class Information:
    def __init__(self, config: Config):
        try:
            self.name = config.get("bot", "name")
        except KeyError:
            self.name = "Bot"
        try:
            self.version = config.get("bot", "version")
        except KeyError:
            self.version = "1.0.0"
        try:
            self.author = config.get("bot", "author")
        except KeyError:
            self.author = "OpenAI"
        try:
            self.country = config.get("bot", "country")
        except KeyError:
            self.country = "France"

    def __call__(self):
        return f"name=\"{self.name}\", version=\"{self.version}\", author=\"{self.author}\", country=\"{self.country}\"\r"
