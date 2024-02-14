import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="ping", description="Command to test the bot's latency.")
    async def ping_command(self, interaction: discord.Interaction):
        try:
            latency = round(self.bot.latency * 1000)

            embed_schema = EmbedSchema(
                title="🏓 Pong!",
                description=f"Latency is `{latency}ms`.",
                color=0xb34760
            )

            embed = EmbedController().build_embed(embed_schema)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.critical(f"Failed to respond to ping command: {e}")
            await interaction.response.send_message("There was an error trying to execute that command!", ephemeral=True)

    @ping_command.error
    async def ping_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    logger.info("Ping command loaded!")