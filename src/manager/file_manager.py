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

# Scalability settings for ban updates
update_batch_size: 5          # Servers to update per batch
batch_delay: 1.0             # Seconds between batches
max_concurrent_updates: 3    # Max concurrent server updates
min_update_interval: 30      # Minimum seconds between updates
"""


class FileManager:

    def __init__(self) -> None:
        self.config = Config()

    # Function to check if the input files are valid
    def check_input(self) -> None:

        # if there is no config file, create one.
        if not os.path.isfile("config.yaml"):
            logger.info("Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            logger.info(
                "Successfully created config.yml, please fill it out and try again."
            )
            exit()

        # If the folder "/src/database" doesn't exist, create it.
        if not os.path.exists("src/database"):
            os.makedirs("src/database")
