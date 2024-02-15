import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.database.schema.server_schema import ServerSchema
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController
from src.database.controller.servers_db_controller import ServersDbController

class BroadcastCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = Config()
        self.servers_db_controller = ServersDbController()

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="broadcast", description="Set the channel to broadcast bans in.")
    async def broadcast_bans(self, interaction: discord.Interaction, channel: discord.TextChannel = None, hidden: bool = False) -> None:
        try:

            if channel is None:
                channel = interaction.channel

            try:
                repo_schema = ServerSchema(interaction.guild.id, channel.id, None)
                #logger.debug(f"Adding channel to the database: {repo_schema.__repr__()}")
                await self.servers_db_controller.insert(repo_schema)
            except Exception as e:
                logger.critical(f"Failed to add channel to the database: {e}")
                await interaction.response.send_message("There was an error trying to add the channel to the database!", ephemeral=hidden)
                return

            embed_schema = EmbedSchema(
                title="Broadcast Channel Added!",
                description="Succesfully set the broadcast channel to the channel below.",
                fields=[
                    {"name": "Channel", "value": f"- {channel.mention} (`{channel.id}`)"},
                    {"name": "Server", "value": f"- {interaction.guild.name} (`{interaction.guild.id}`)"},
                ],
                color=0x00ff00
            )

            embed = await EmbedController().build_embed(embed_schema)
            await interaction.response.send_message(embed=embed, ephemeral=hidden)
        except Exception as e:
            logger.critical(f"Failed to respond to broadcast command: {e}")
            await interaction.response.send_message("There was an error trying to execute that command!", ephemeral=hidden)

    @broadcast_bans.error
    async def broadcast_bans_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BroadcastCommand(bot))
    logger.info("Broadcast command loaded!")