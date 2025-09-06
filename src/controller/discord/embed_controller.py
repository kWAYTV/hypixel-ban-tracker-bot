from datetime import datetime

import discord
from loguru import logger

from src.controller.discord.schema.embed_schema import EmbedSchema
from src.helper.config import Config


class EmbedController:
    """
    A class that handles the creation of Discord embeds.
    """

    def __init__(self) -> None:
        self.config = Config()

    async def build_embed(self, embed_schema: EmbedSchema) -> discord.Embed:
        """
        Builds a Discord embed based on the provided embed schema.

        Args:
            embed_schema (EmbedSchema): The schema containing the details of the embed.

        Returns:
            discord.Embed: The built Discord embed.
        """
        try:
            schema = embed_schema.get_schema()
            embed = discord.Embed(
                title=schema["title"],
                description=schema["description"],
                color=schema["color"],
            )

            for field in schema["fields"]:
                value = field["value"]

                # Convert non-string values to strings
                if not isinstance(value, str):
                    value = str(value)

                if value == "None" or value is None:
                    continue

                embed.add_field(
                    name=field["name"], value=value, inline=field.get("inline", False)
                )

            await self.set_defaults(embed, schema)
            embed.timestamp = datetime.utcnow()

            return embed

        except Exception as e:
            logger.error(f"Failed to build embed: {e}")

    async def set_defaults(self, embed: discord.Embed, schema: dict) -> None:
        """
        Sets default values for various properties of the embed.

        Args:
            embed (discord.Embed): The Discord embed to set the default values for.
            schema (dict): The schema containing the default values.

        Returns:
            None
        """
        author_name = schema.get("author_name", self.config.app_name)
        author_icon_url = schema.get("author_icon_url", self.config.app_logo)
        author_url = schema.get("author_url", self.config.app_url)
        footer_text = schema.get("footer_text", self.config.app_name)
        footer_icon_url = schema.get("footer_icon_url", self.config.app_logo)
        image_url = schema.get("image_url", self.config.rainbow_line_gif)
        thumbnail_url = schema.get("thumbnail_url", self.config.app_logo)

        embed.set_author(name=author_name, icon_url=author_icon_url, url=author_url)
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)
