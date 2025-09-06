import os

from discord.ext import commands
from loguru import logger
from pyfiglet import Figlet
from pystyle import Center, Colorate, Colors

from src.helper.config import Config


class OnReady(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self) -> None:

        os.system("cls||clear")

        logo = Figlet(font="big").renderText(self.config.app_name)
        centered_logo = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1))
        divider = Center.XCenter(
            Colorate.Vertical(
                Colors.white_to_blue, "────────────────────────────────────────────", 1
            )
        )
        print(f"{centered_logo}\n{divider}\n\n")

        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return logger.info("On ready event registered!")
