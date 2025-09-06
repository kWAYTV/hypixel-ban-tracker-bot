from itertools import cycle

from discord.ext import commands

from src.helper.config import Config


class BotStatus:
    """
    Represents the status of the Discord bot.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
        config (Config): The configuration object.
        sentences (list): A list of lambda functions that generate status sentences.
        status_generator (itertools.cycle): An iterator that cycles through the status sentences.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = Config()

        self.sentences = [
            lambda self: (
                f"Holding {len(self.bot.guilds)} guilds & "
                f"{sum(guild.member_count for guild in self.bot.guilds)} users."
            ),
            lambda self: f"Hey! My name is {self.config.app_name}.",
            lambda self: "Broadcasting Hypixel bans!",
            lambda self: "People taking the L.",
        ]

        self.status_generator = cycle(self.sentences)

    async def get_status_message(self) -> str:
        """
        Retrieves the next status message.

        Returns:
            str: The next status message.
        """
        next_status_message = next(self.status_generator)
        return next_status_message(self)
