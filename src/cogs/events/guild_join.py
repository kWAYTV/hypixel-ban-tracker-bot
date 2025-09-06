from discord.ext import commands
from loguru import logger


class GuildJoin(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> None:

        try:
            # Sync the commands
            await self.bot.tree.sync()
        except Exception as e:
            logger.critical(f"❌ Failed to sync slash commands: {e}")
            return

        # Send a DM to the guild owner
        try:
            await guild.owner.send(
                "Hello `{guild.owner.name}`, your guild `{guild.name}` "
                "has successfully synced commands with the bot!"
            )
        except Exception:
            logger.error(
                "❌ Couln't send a DM to the guild owner of "
                f"{guild.name} ({guild.owner.id})."
            )
            return

        # Log the event
        logger.info(f"✅ Bot joined Guild: {guild.name}. ({guild.id})")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildJoin(bot))
    return logger.info("On guild join event registered!")
