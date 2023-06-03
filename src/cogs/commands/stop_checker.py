import discord
from colorama import Fore
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.helper.config import Config

class StopChecker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.logger = Logger(self.bot)

    # Ping bot command  
    @app_commands.command(name="stopchecker", description="Command to stop sending bans to this channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def stop_checker(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.channel_id in Config().tracker_channels:
            Config().remove_tracker_channel(interaction.channel_id)
            await interaction.followup.send("✅ Channel removed! I will now stop sending bans to this channel.")
            self.logger.log("INFO", f"Removed channel {interaction.channel_id} from tracker channels list.")
            await self.logger.discord_log(f"Removed channel {interaction.channel_id} from tracker channels list.")
        else:
            await interaction.followup.send("❌ Channel not found! That channel it's not into the list.")

    @stop_checker.error
    async def stop_checker_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StopChecker(bot))
    return Logger().log("INFO", "Ping command loaded!")