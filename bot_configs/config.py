# -------configuration constants-----------
from configparser import ConfigParser


class ConfigData:
    FILENAME = "bot_configs/config.ini"

    def __init__(self):
        parser = ConfigParser()
        parser.read(self.FILENAME)

        # add your configuration constants here:
        self.PYTHON_PATH = parser["SETTINGS"]["PYTHON_PATH"]
        self.BOT_TOKEN = parser["TOKENS"]["BOT_TOKEN"]
