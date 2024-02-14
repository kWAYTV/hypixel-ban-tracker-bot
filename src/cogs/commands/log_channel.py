import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class LogChannelCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="log_channel", description="Set the bot log channel.")
    async def log_channel(self, interaction: discord.Interaction, log_channel: discord.TextChannel = None, hidden: bool = False) -> None:
        try:

            if log_channel is None:
                log_channel = interaction.channel

            try:
                self.config.change_value("logs_channel", log_channel.id)
            except Exception as e:
                logger.critical(f"Failed to change value in config.yaml: {e}")
                await interaction.response.send_message("There was an error trying to write the config file!", ephemeral=hidden)
                return

            embed_schema = EmbedSchema(
                title="Log channel update",
                description="Succesfully set the log channel to the chanel below.",
                fields=[
                    {
                        "name": "New logs channel",
                        "value": f"- {log_channel.mention} (`{log_channel.id}`)"
                    }
                ],
                color=0x00ff00
            )

            embed = EmbedController().build_embed(embed_schema)
            await interaction.response.send_message(embed=embed, ephemeral=hidden)
        except Exception as e:
            logger.critical(f"Failed to respond to info command: {e}")
            await interaction.response.send_message("There was an error trying to execute that command!", ephemeral=hidden)

    @log_channel.error
    async def log_channel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LogChannelCommand(bot))
    logger.info("Log channel command loaded!")