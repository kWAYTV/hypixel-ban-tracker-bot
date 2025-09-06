from discord.ext import commands
from loguru import logger

from src.database.controller.servers_db_controller import ServersDbController


class GuildRemove(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild) -> None:
        ServersDbController().delete(guild.id)
        logger.info(f"The bot left the guild {guild.name} ({guild.id}).")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildRemove(bot))
    return logger.info("On guild leave event registered!")
