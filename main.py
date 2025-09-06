# Imports
import os
import sys
from traceback import format_exc

import discord
from discord.ext import commands
from loguru import logger

from src.database.loader import DatabaseLoader
from src.helper.config import Config
from src.manager.file_manager import FileManager

# Set logging system handler
logger.add(Config().log_file, mode="w+")


# Define the bot & load the commands, events and loops
class Bot(commands.Bot):
    def __init__(self) -> None:
        self.file_manager = FileManager()
        super().__init__(
            command_prefix=Config().bot_prefix,
            help_command=None,
            intents=discord.Intents.all(),
        )

    # Function to load the extensions
    async def setup_hook(self) -> None:
        try:
            os.system("cls||clear")
            logger.info("Starting bot...")

            # Check for file inputs
            logger.debug("Checking for file inputs...")
            self.file_manager.check_input()

            # Load the cogs
            logger.debug("Loading cogs...")
            for filename in os.listdir("./src/cogs/commands"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.commands.{filename[:-3]}")

            # Load the events
            logger.debug("Loading events...")
            for filename in os.listdir("./src/cogs/events"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.events.{filename[:-3]}")

            # Load the loops
            logger.debug("Loading loops...")
            for filename in os.listdir("./src/cogs/loops"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.loops.{filename[:-3]}")

            # Set-up the database
            logger.debug("Setting up databases...")
            await DatabaseLoader().setup()

            # Done!
            logger.info("Setup completed!")
        except Exception:
            logger.critical(f"Error setting up bot: {format_exc()}")
            sys.exit(1)

    # Function to shutdown the bot
    async def close(self) -> None:
        await super().close()


# Run the bot
if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run(Config().bot_token)
    except KeyboardInterrupt:
        logger.critical("Goodbye!")
        sys.exit(0)
    except Exception:
        logger.critical(f"Error running bot: {format_exc()}")
        sys.exit(1)
