from discord.ext import commands
from src.util.logger import Logger

class GuildJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=guild)
        self.logger.log("INFO", f"Synced commands with {guild.name}.")
        await self.logger.discord_log(f"Synced commands with {guild.name}.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildJoin(bot))
    return Logger().log("INFO", "On guild join event registered!")