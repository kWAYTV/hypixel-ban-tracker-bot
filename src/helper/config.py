import discord
import yaml
from loguru import logger
from yaml import SafeLoader


class Config:
    def __init__(self) -> None:
        self.config_path = "config.yaml"

        with open(self.config_path, "r", encoding="utf-8") as file:
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
        self.dev_guild_id = discord.Object(int(self.config["dev_guild_id"]))

        # Logs
        self.log_file = self.config["log_file"]

        # Scalability settings
        self.update_batch_size = self.config.get("update_batch_size", 5)
        self.batch_delay = self.config.get("batch_delay", 1.0)
        self.max_concurrent_updates = self.config.get("max_concurrent_updates", 3)
        self.min_update_interval = self.config.get("min_update_interval", 30)

    # Function to change a value in config.yaml
    def change_value(self, key, value) -> bool:
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                config = yaml.load(file, Loader=SafeLoader)
            config[key] = value
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(config, file)
            logger.info(
                f"Changed value in config.yaml: {key} -> {value}, the file was rewritten."
            )
            return True
        except Exception as e:
            logger.critical(f"Failed to change value in config.yaml: {e}")
            return False
