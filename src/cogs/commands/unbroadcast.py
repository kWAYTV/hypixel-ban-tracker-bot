import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from src.controller.discord.embed_controller import EmbedController
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.database.controller.servers_db_controller import ServersDbController
from src.database.schema.server_schema import ServerSchema
from src.helper.config import Config


class UnbroadcastCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = Config()
        self.servers_db_controller = ServersDbController()

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="unbroadcast", description="Remove this server from ban broadcasts."
    )
    async def unbroadcast_bans(
        self, interaction: discord.Interaction, hidden: bool = False
    ) -> None:
        try:
            server_exists = await self.servers_db_controller.get(interaction.guild.id)

            if not server_exists:
                embed_schema = EmbedSchema(
                    title="Not Subscribed!",
                    description="This server is not currently subscribed to ban broadcasts.",
                    color=0xFFA500,
                )
            else:
                await self.servers_db_controller.delete(interaction.guild.id)
                embed_schema = EmbedSchema(
                    title="Broadcast Channel Removed!",
                    description="Successfully removed this server from ban broadcasts.",
                    fields=[
                        {
                            "name": "Server",
                            "value": f"- {interaction.guild.name} (`{interaction.guild.id}`)",
                        },
                    ],
                    color=0xFF0000,
                )

            embed = await EmbedController().build_embed(embed_schema)
            await interaction.response.send_message(embed=embed, ephemeral=hidden)
        except Exception as e:
            logger.critical(f"Failed to respond to unbroadcast command: {e}")
            await interaction.response.send_message(
                "There was an error trying to execute that command!", ephemeral=hidden
            )

    @unbroadcast_bans.error
    async def unbroadcast_bans_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f"You don't have the necessary permissions to use this command.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"An error occurred: {error}", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnbroadcastCommand(bot))
    logger.info("Unbroadcast command loaded!")
