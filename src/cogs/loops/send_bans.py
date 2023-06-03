from itertools import cycle
from src.util.logger import Logger
from src.helper.config import Config
from discord.ext import commands, tasks
from src.hypixel.ban_checker import BanChecker

class SendBansLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.banchecker = BanChecker()
        self.logger = Logger()
        self.config = Config()
        self.send_bans.start()

    # Dynamic activity
    status = cycle(["Hypixel Bans", "Cheaters", "Hackers", "Rulebreakers", "Banned Players"])
    @tasks.loop(seconds=0.1)
    async def send_bans(self):
        bans = self.banchecker.check_bans()
        if bans:
            [await self.bot.get_channel(channel_id).send(embed=embed) for embed in bans for channel_id in self.config.tracker_channels]
            self.logger.log("INFO", f"Sent {len(bans)} ban(s) to {len(self.config.tracker_channels)} channel(s)!")

    @send_bans.before_loop
    async def before_change_status(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SendBansLoop(bot))
    return Logger().log("INFO", "Ban checker loop loaded!")