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
            embed = discord.Embed(title="✅ Channel removed!", description="I will now stop sending bans to this channel!", color=0xb34760)
            embed.set_footer(text="Hypixel Ban Tracker - discord.gg/kws")
            embed.set_image(url=self.config.hypixel_logo)
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)
            self.logger.log("INFO", f"Removed channel {interaction.channel_id} from tracker channels list.")
            await self.logger.discord_log(f"Removed channel {interaction.channel_id} from tracker channels list.")
        else:
            embed = discord.Embed(title="❌ Channel not found!", description="That channel it's not into the list!", color=0xb34760)
            embed.set_footer(text="Hypixel Ban Tracker - discord.gg/kws")
            embed.set_image(url=self.config.hypixel_logo)
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)

    @stop_checker.error
    async def stop_checker_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StopChecker(bot))
    return Logger().log("INFO", "Ping command loaded!")