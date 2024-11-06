from configparser import ConfigParser


class Config:
    def __init__(self, config_file="bot.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get(self, section, key):
        """
        Get a value from the config file.

        :param section: The section of the config file to look in.
        :param key: The key to look for in the section.
        :return: The value of the key in the section.
        If the section or key does not exist, a `KeyError` is raised.
        """
        return self.config[section][key]
