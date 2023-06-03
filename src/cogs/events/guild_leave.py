from discord.ext import commands
from src.util.logger import Logger
from src.helper.config import Config

class GuildLeave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(self.bot)

    # Function to check if the bot is still in the channel
    async def check_channels(self):
        # Check every channel in the config if the bot is still in it
        for channel_id in Config().tracker_channels:
            if not self.bot.get_channel(channel_id):
                Config().remove_tracker_channel(channel_id)
                self.logger.log("INFO", f"Removed channel {channel_id} from the config.")
            else:
                self.logger.log("INFO", f"Channel {channel_id} is still in the bot's eyes.")

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        self.check_channels()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildLeave(bot))
    return Logger().log("INFO", "On guild leave event registered!")