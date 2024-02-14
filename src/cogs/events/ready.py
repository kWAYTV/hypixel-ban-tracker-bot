import os
from loguru import logger
from pyfiglet import Figlet
from discord.ext import commands
from src.helper.config import Config
from pystyle import Colors, Colorate, Center

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self):

        os.system("cls||clear")

        logo = Figlet(font="big").renderText(self.config.app_name)
        centered_logo = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1))
        divider = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────", 1))
        print(f"{centered_logo}\n{divider}\n\n")

        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return logger.info("On ready event registered!")