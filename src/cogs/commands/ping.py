import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="ping", description="Command to test the bot's latency.")
    async def ping_command(self, interaction: discord.Interaction) -> None:
        try:
            latency = round(self.bot.latency * 1000)

            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Latency is `{latency}ms`.",
                color=0xB34760,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.critical(f"Failed to respond to ping command: {e}")
            await interaction.response.send_message(
                "There was an error trying to execute that command!", ephemeral=True
            )

    @ping_command.error
    async def ping_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "You don't have the necessary permissions to use this command.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"An error occurred: {error}", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    logger.info("Ping command loaded!")
