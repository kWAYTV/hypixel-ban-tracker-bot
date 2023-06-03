# Imports
import discord, os
from discord.ext import commands
from colorama import Fore
from src.helper.config import Config
from src.util.logger import Logger

# Define the bot & load the commands, events and loops
class Bot(commands.Bot):
    def __init__(self) -> None:
        self.logger = Logger()
        super().__init__(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        self.logger.clear()
        self.logger.log("INFO", f"Starting bot...")
        self.logger.log("INFO", "Loading cogs...")
        for filename in os.listdir("./src/cogs/commands"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.commands.{filename[:-3]}")
        self.logger.log("INFO", "Loading events...")
        for filename in os.listdir("./src/cogs/events"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.events.{filename[:-3]}")
        self.logger.log("INFO", "Loading loops...")
        for filename in os.listdir("./src/cogs/loops"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"src.cogs.loops.{filename[:-3]}")

# Define the clients
bot = Bot()

# Run the bot
if __name__ == "__main__":
    try:
        bot.run(Config().discord_token)
    except KeyboardInterrupt:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Powering off the bot...")
        exit()