import discord
from colorama import Fore
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.helper.config import Config

class StartChecker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.logger = Logger(self.bot)

    # Ping bot command  
    @app_commands.command(name="startchecker", description="Command to start sending bans to this channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def start_checker(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.channel_id not in Config().tracker_channels:
            Config().add_tracker_channel(interaction.channel_id)
            embed = discord.Embed(title="✅ Channel added!", description="I will now send bans to this channel!", color=0xb34760)
            embed.set_author(name="Hypixel Ban Tracker")
            embed.set_footer(text="Hypixel Ban Tracker - discord.gg/kws")
            embed.set_image(url=self.config.hypixel_logo)
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)
            self.logger.log("INFO", f"Added channel {interaction.channel_id} to tracker channels list.")
            await self.logger.discord_log(f"Added channel {interaction.channel_id} to tracker channels list.")
        else:
            embed = discord.Embed(title="❌ Channel already added!", description="I am already sending bans to this channel!", color=0xb34760)
            embed.set_author(name="Hypixel Ban Tracker")
            embed.set_footer(text="Hypixel Ban Tracker - discord.gg/kws")
            embed.set_image(url=self.config.hypixel_logo)
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)

    @start_checker.error
    async def start_checker_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StartChecker(bot))
    return Logger().log("INFO", "Ping command loaded!")