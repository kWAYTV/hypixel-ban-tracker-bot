from loguru import logger
from discord.ext import commands, tasks
from src.controller.hypixel.bans_controller import BansController

class BansLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bans_controller = BansController(bot)
        self.check_bans.start()

    @tasks.loop(seconds=30)
    async def check_bans(self) -> None:
        try:
            await self.bans_controller.check_and_update_bans()
        except Exception as e:
            logger.error(f"Error while updating bans: {e}")

    @check_bans.before_loop
    async def before_check_bans(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BansLoop(bot))
    logger.info("Bans loop loaded!")
