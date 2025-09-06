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
                # Try to clean up the message panel before removing from database
                message_deleted = False
                if server_exists.message_id:
                    try:
                        channel = self.bot.get_channel(server_exists.channel_id)
                        if channel:
                            message = await channel.fetch_message(
                                server_exists.message_id
                            )
                            if message:
                                await message.delete()
                                message_deleted = True
                                logger.info(
                                    f"Deleted ban panel message for server {interaction.guild.id}"
                                )
                    except Exception as e:
                        logger.warning(
                            f"Could not delete ban panel message for server {interaction.guild.id}: {e}"
                        )
                        # Continue with unsubscription even if message deletion fails

                # Remove server from database
                await self.servers_db_controller.delete(interaction.guild.id)

                # Update success message based on cleanup result
                description = "Successfully removed this server from ban broadcasts."
                if message_deleted:
                    description += "\n✅ Ban panel message was also cleaned up."
                elif server_exists.message_id:
                    description += "\n⚠️ Ban panel message could not be found (may have been deleted manually)."

                embed_schema = EmbedSchema(
                    title="Broadcast Channel Removed!",
                    description=description,
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
