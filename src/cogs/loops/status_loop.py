import discord
from loguru import logger
from discord.ext import commands, tasks
from src.helper.status import BotStatus as Status

class StatusLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.status = Status(self.bot)
        self.change_status.start()

    @tasks.loop(seconds=30)
    async def change_status(self):
        status_message = await self.status.get_status_message()
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name=status_message))

    @change_status.before_loop
    async def before_change_status(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusLoop(bot))
    return logger.info("Status loop loaded!")