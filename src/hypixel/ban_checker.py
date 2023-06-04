import discord, requests, math, time
from datetime import datetime
from src.helper.config import Config

class BanChecker:
    """A class to check for bans in Hypixel"""
    def __init__(self) -> None:
        """Constructor for BanChecker class"""
        self.old_wd_bans = None
        self.old_staff_bans = None
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "kys"})
        self.config = Config()

    def create_embed(self, ban_diff, enforcer, color, daily_total, total_bans):
        """Helper function to create embed object"""
        embed = discord.Embed(title="New ban detected!", color=color, description=f"<t:{math.floor(time.time())}:R>")
        embed.set_author(name=f"{enforcer} banned {ban_diff} player{'s'[:ban_diff^1]}.")
        embed.set_thumbnail(url=self.config.hypixel_logo)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"Bans today: {daily_total} - Total bans: {total_bans}")
        return embed

    def get_current_stats(self):
        """Fetch current stats from the API"""
        response = self.session.get('https://api.plancke.io/hypixel/v1/punishmentStats')
        return response.json().get('record', {})

    def check_bans(self):
        """Check for bans and return a list of embeds"""
        curr_stats = self.get_current_stats()
        wd_bans = curr_stats.get("watchdog_total")
        staff_bans = curr_stats.get("staff_total")
        daily_total = curr_stats.get("staff_rollingDaily") + curr_stats.get("watchdog_rollingDaily")
        total_bans = curr_stats.get("staff_total") + curr_stats.get("watchdog_total")
        embeds = []

        if self.old_wd_bans is not None and self.old_staff_bans is not None:
            wd_ban_diff = wd_bans - self.old_wd_bans
            staff_ban_diff = staff_bans - self.old_staff_bans

            if wd_ban_diff > 0:
                embeds.append(self.create_embed(wd_ban_diff, "Watchdog", discord.Color.from_rgb(247, 57, 24), daily_total, total_bans))
            if staff_ban_diff > 0:
                embeds.append(self.create_embed(staff_ban_diff, "Staff", discord.Color.from_rgb(247, 229, 24), daily_total, total_bans))

        self.old_wd_bans = wd_bans
        self.old_staff_bans = staff_bans

        return embeds