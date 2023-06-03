import discord
from colorama import Fore
from itertools import cycle
from src.util.logger import Logger
from src.helper.config import Config
from discord.ext import commands, tasks

class CheckChannels(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = Logger()
        self.check_channels.start()

    @tasks.loop(seconds=60)
    # Function to check if the bot is still in the channel
    async def check_channels(self):
        # Check every channel in the config if the bot is still in it
        for channel_id in Config().tracker_channels:
            if not self.bot.get_channel(channel_id) or self.bot.get_channel(channel_id) is None:
                Config().remove_tracker_channel(channel_id)
                self.logger.log("INFO", f"Removed channel {channel_id} from the config.")

    @check_channels.before_loop
    async def before_check_channels(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CheckChannels(bot))
    return Logger().log("INFO", "Check channels loop loaded!")