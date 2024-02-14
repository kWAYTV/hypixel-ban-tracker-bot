import discord
from loguru import logger
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @app_commands.command(name="info", description="Information about the bot.")
    async def info_command(self, interaction: discord.Interaction, hidden: bool = False):
        try:
            latency = round(self.bot.latency * 1000)
            embed = discord.Embed(
                description=f":information_source: Some information about the bot.",
                color=0x000000
            )
            embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)

            embed.add_field(name=":desktop: Servers", value=f"```{len(self.bot.guilds)}```", inline=False)
            embed.add_field(name=":busts_in_silhouette: Users", value=f"```{len(self.bot.users)}```", inline=False)
            embed.add_field(name=":ping_pong: Latency", value=f"```{latency} ms```", inline=False)
            embed.add_field(name=":gear: Version", value=f"```{self.config.app_version}```", inline=False)

            embed.set_footer(text=self.config.app_name, icon_url=self.config.app_logo)
            embed.set_thumbnail(url=self.config.app_logo)
            embed.set_image(url=self.config.rainbow_line_gif)
            embed.timestamp = datetime.utcnow()

            await interaction.response.send_message(embed=embed, ephemeral=hidden)
        except Exception as e:
            logger.critical(f"Failed to respond to info command: {e}")
            await interaction.response.send_message("There was an error trying to execute that command!", ephemeral=hidden)

    @info_command.error
    async def info_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
    logger.info("Info command loaded!")