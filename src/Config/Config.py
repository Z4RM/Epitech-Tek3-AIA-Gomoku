from configparser import ConfigParser


class Config:
    def __init__(self, config_file="config.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get(self, section, key):
        return self.config[section][key]
