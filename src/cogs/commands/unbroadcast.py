import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from src.database.controller.servers_db_controller import ServersDbController
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
        self, interaction: discord.Interaction, hidden: bool = True
    ) -> None:
        try:
            server_exists = await self.servers_db_controller.get(interaction.guild.id)

            if not server_exists:
                embed = discord.Embed(
                    title="Not Subscribed!",
                    description="This server is not currently subscribed to ban broadcasts.",
                    color=0xFFA500,
                )
            else:
                # Try to clean up the message panel before removing from database
                message_deleted = await self._cleanup_message_panel(
                    server_exists, interaction.guild.id
                )

                # Remove server from database
                await self.servers_db_controller.delete(interaction.guild.id)

                # Update success message based on cleanup result
                description = "Successfully removed this server from ban broadcasts."
                if message_deleted:
                    description += "\n✅ Ban panel message was also cleaned up."
                elif server_exists.message_id:
                    description += (
                        "\n⚠️ Ban panel message could not be found "
                        "(may have been deleted manually)."
                    )

                embed = discord.Embed(
                    title="Broadcast Channel Removed!",
                    description=description,
                    color=0xFF0000,
                )

                embed.add_field(
                    name="Server",
                    value=f"- {interaction.guild.name} (`{interaction.guild.id}`)",
                    inline=False,
                )

            # embed is already created above
            await interaction.response.send_message(embed=embed, ephemeral=hidden)
        except Exception as e:
            logger.critical(f"Failed to respond to unbroadcast command: {e}")
            await interaction.response.send_message(
                "There was an error trying to execute that command!", ephemeral=hidden
            )

    async def _cleanup_message_panel(self, server_schema, guild_id: int) -> bool:
        """Clean up the message panel and return success status."""
        if not server_schema.message_id:
            return False

        try:
            channel = self.bot.get_channel(server_schema.channel_id)
            if not channel:
                return False

            message = await channel.fetch_message(server_schema.message_id)
            if not message:
                return False

            await message.delete()
            logger.info(f"Deleted ban panel message for server {guild_id}")
            return True

        except Exception as e:
            logger.warning(
                f"Could not delete ban panel message for server {guild_id}: {e}"
            )
            return False

    @unbroadcast_bans.error
    async def unbroadcast_bans_error(
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnbroadcastCommand(bot))
    logger.info("Unbroadcast command loaded!")
