import asyncio
import math
import time

import requests
from discord import Embed
from discord.ext import commands
from loguru import logger

from src.controller.discord.embed_controller import EmbedController
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.database.controller.servers_db_controller import ServersDbController
from src.helper.config import Config


class BansController:
    """
    Controller class for managing bans on Hypixel.

    Methods:
        get_current_stats: Retrieves the current ban statistics from the Hypixel API.
        update_recent_bans: Updates the list of recent ban messages.
        create_embed: Creates an embed object for displaying ban information.
        check_and_update_bans: Checks for ban updates and updates the ban messages in the specified channels.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config = Config()

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "kwayservices.top"})

        self.old_wd_bans = None
        self.old_staff_bans = None
        self.recent_bans = []
        self.last_update_time = 0

        self.servers_db_controller = ServersDbController()
        self.url = "https://api.plancke.io/hypixel/v1/punishmentStats"

    async def get_current_stats(self) -> dict:
        response = self.session.get(self.url)
        return response.json().get("record", {})

    async def update_recent_bans(self, wd_ban_diff, staff_ban_diff) -> None:
        if wd_ban_diff > 0:
            self.recent_bans.append(
                f"⛔ Watchdog -> {wd_ban_diff} player{'s' if wd_ban_diff > 1 else ''}."
            )
        if staff_ban_diff > 0:
            self.recent_bans.append(
                f"🔨 Staff -> {staff_ban_diff} player{'s' if staff_ban_diff > 1 else ''}."
            )
        self.recent_bans = self.recent_bans[-10:]  # Keep only the last 5 incidents

    async def create_embed(self, curr_stats, last_update, recent_bans) -> Embed:
        daily_watchdog = curr_stats.get("watchdog_rollingDaily", 0)
        daily_staff = curr_stats.get("staff_rollingDaily", 0)
        daily_total = daily_watchdog + daily_staff
        total_bans = curr_stats.get("watchdog_total", 0) + curr_stats.get(
            "staff_total", 0
        )
        watchdog_last_min = curr_stats.get("watchdog_lastMinute", 0)
        recent_bans_text = "\n".join(recent_bans) if recent_bans else "No recent bans"

        embed_schema = EmbedSchema(
            title="Bans Tracker",
            description="This is a live tracker of bans on Hypixel.",
            fields=[
                {
                    "name": "Daily Watchdog",
                    "value": f"`{daily_watchdog:,}`",
                    "inline": True,
                },
                {"name": "Daily Staff", "value": f"`{daily_staff:,}`", "inline": True},
                {
                    "name": "Watchdog Last Min",
                    "value": f"`{watchdog_last_min}`",
                    "inline": True,
                },
                {"name": "Daily Total", "value": f"`{daily_total:,}`", "inline": True},
                {"name": "Total Bans", "value": f"`{total_bans:,}`", "inline": True},
                {"name": "Updated", "value": f"<t:{last_update}:R>", "inline": True},
                {"name": "Recent", "value": f"```{recent_bans_text}```"},
            ],
            color=0x00FF00,
        )
        return await EmbedController().build_embed(embed_schema)

    async def check_and_update_bans(self) -> None:
        curr_stats = await self.get_current_stats()
        wd_bans = curr_stats.get("watchdog_total", 0)
        staff_bans = curr_stats.get("staff_total", 0)

        if self.old_wd_bans is None or self.old_staff_bans is None:
            self.old_wd_bans, self.old_staff_bans = wd_bans, staff_bans
            return

        wd_ban_diff = wd_bans - self.old_wd_bans
        staff_ban_diff = staff_bans - self.old_staff_bans

        # Check minimum interval to prevent spam
        current_time = time.time()
        if current_time - self.last_update_time < self.config.min_update_interval:
            return

        # Only update if there are actual changes
        if wd_ban_diff <= 0 and staff_ban_diff <= 0:
            return

        await self.update_recent_bans(wd_ban_diff, staff_ban_diff)
        last_update = math.floor(current_time)
        self.last_update_time = current_time

        # Get all servers and process in scalable batches
        all_servers = await self.servers_db_controller.get_all()
        if not all_servers:
            return

        await self.process_servers_in_batches(all_servers, curr_stats, last_update)

        self.old_wd_bans, self.old_staff_bans = wd_bans, staff_bans

    async def process_servers_in_batches(self, servers, curr_stats, last_update):
        """Process servers in batches to avoid rate limiting"""
        batch_size = self.config.update_batch_size
        batch_delay = self.config.batch_delay
        max_concurrent = self.config.max_concurrent_updates

        for i in range(0, len(servers), batch_size):
            batch = servers[i : i + batch_size]

            # Process batch concurrently but with controlled concurrency
            tasks = []
            for server_schema in batch:
                task = self.update_single_server(server_schema, curr_stats, last_update)
                tasks.append(task)

            # Execute batch with semaphore to control concurrency
            semaphore = asyncio.Semaphore(max_concurrent)

            async def limited_update(task):
                async with semaphore:
                    return await task

            await asyncio.gather(*[limited_update(task) for task in tasks])

            # Add delay between batches (except for last batch)
            if i + batch_size < len(servers):
                await asyncio.sleep(batch_delay)

    async def update_single_server(self, server_schema, curr_stats, last_update):
        """Update a single server's ban panel"""
        try:
            channel = self.bot.get_channel(server_schema.channel_id)
            if not channel:
                await self.servers_db_controller.delete(server_schema.server_id)
                return

            embed = await self.create_embed(curr_stats, last_update, self.recent_bans)
            message = (
                await channel.fetch_message(server_schema.message_id)
                if server_schema.message_id
                else None
            )

            if message:
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                await self.servers_db_controller.update_message_id(
                    server_schema.server_id, message.id
                )

        except Exception as e:
            logger.warning(f"Failed to update server {server_schema.server_id}: {e}")
            # Could implement retry logic here if needed
