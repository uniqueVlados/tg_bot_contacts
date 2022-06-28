# -------configuration constants-----------
from configparser import ConfigParser


class ConfigData:
    FILENAME = "config.ini"

    def __init__(self):
        parser = ConfigParser()
        parser.read(self.FILENAME)

        # add your configuration constants here:
        self.BOT_TOKEN = parser["TOKENS"]["BOT_TOKEN"]
        self.DB_URI = parser["SETTINGS"]["DB_URI"]
        self.LINK_AGR = parser["URL"]["LINK_AGREEMENT"]
        self.FILENAME_CITIES = parser["FILES"]["FILENAME_CITIES"]
        # self.PYTHON_PATH = parser["SETTINGS"]["PYTHON_PATH"]
