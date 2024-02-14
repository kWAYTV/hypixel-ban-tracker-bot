import discord
from loguru import logger
from datetime import datetime
from discord.ext import commands
from src.helper.config import Config

class Logger:
    """
    A class that handles logging and sending messages to Discord channels and users.
    """

    def __init__(self, bot: commands.Bot = None):
        self.bot = bot
        self.config = Config()

    async def discord_log(self, description: str):
        """
        Sends a log message to the configured Discord logs channel.

        Args:
            description (str): The description of the log message.
        """
        channel = self.bot.get_channel(self.config.logs_channel)
        if channel:
            embed = discord.Embed(title=self.config.app_name, description=f"```{description}```")
            embed.set_thumbnail(url=self.config.app_logo)
            embed.set_image(url=self.config.rainbow_line_gif)
            embed.set_footer(text=f"{self.config.app_name_branded}", icon_url=self.config.app_logo)
            embed.timestamp = datetime.utcnow()
            await channel.send(embed=embed)
        else:
            logger.error(f"Could not find the logs channel with id {self.config.logs_channel}")

    async def dm_user(self, userid: int, message: str):
        """
        Sends a direct message to a user with the specified user ID.

        Args:
            userid (int): The ID of the user to send the message to.
            message (str): The message to send.
        """
        user = await self.bot.fetch_user(userid)
        if user:
            await user.send(message)
        else:
            logger.error(f"Could not find the user with id {userid}")