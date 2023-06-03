import discord
from colorama import Fore
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Ping bot command  
    @app_commands.command(name="ping", description="Command to test the bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def ping_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        latency = round(self.bot.latency *  1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Hey! My latency is `{latency}` ms!", color=0xb34760)
        embed.set_footer(text="Hypixel Ban Tracker - discord.gg/kws")
        embed.set_image(url=self.config.hypixel_logo)
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed)

    @ping_command.error
    async def ping_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    return Logger().log("INFO", "Ping command loaded!")