import os
from loguru import logger
from src.helper.config import Config

defaultConfig = """
app_logo: https://i.imgur.com/qXuAK9O.png
app_name: Hypixel
app_url: https://kwayservices.top
app_version: 0.2
bot_prefix: .
bot_token: 
dev_guild_id: 
log_file: hypixel.log
logs_channel: 
"""

class FileManager:

    def __init__(self):
        self.config = Config()

    # Function to check if the input files are valid
    def check_input(self):

        # if there is no config file, create one.
        if not os.path.isfile("config.yaml"):
            logger.info("Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            logger.info("Successfully created config.yml, please fill it out and try again.")
            exit()

        # If the folder "/src/database" doesn't exist, create it.
        if not os.path.exists("src/database"):
            os.makedirs("src/database")