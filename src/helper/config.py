import discord, yaml
from loguru import logger
from yaml import SafeLoader

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        # Rainbow line gif
        self.rainbow_line_gif: str = "https://i.imgur.com/mnydyND.gif"

        # App info
        self.app_logo: str = self.config["app_logo"]
        self.app_url: str = self.config["app_url"]
        self.app_name: str = self.config["app_name"]
        self.app_name_branded: str = f"{self.app_name} • {self.app_url}"
        self.app_version: str = self.config["app_version"]

        # Discord bot
        self.bot_prefix = self.config["bot_prefix"]
        self.bot_token: str = self.config["bot_token"]
        self.logs_channel: int = int(self.config["logs_channel"])
        self.dev_guild_id = discord.Object(int(self.config["dev_guild_id"]))

        # Logs
        self.log_file = self.config["log_file"]

    # Function to change a value in config.yaml
    def change_value(self, key, value):
        try:
            with open("config.yaml", "r") as file:
                config = yaml.load(file, Loader=SafeLoader)
            config[key] = value
            with open("config.yaml", "w") as file:
                yaml.dump(config, file)
            return logger.info(f"Changed value in config.yaml: {key} -> {value}, the file was rewritten.")
        except Exception as e:
            logger.critical(f"Failed to change value in config.yaml: {e}")
            return False