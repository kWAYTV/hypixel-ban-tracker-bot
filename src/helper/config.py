from yaml import SafeLoader
import yaml

class Config():
    def __init__(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.hypixel_logo = "https://i.imgur.com/qXuAK9O.png"
            self.discord_token = self.config["discord_token"]
            self.bot_prefix = self.config["bot_prefix"]
            self.logs_channel = int(self.config["logs_channel"])
            self.tracker_channels = self.config["tracker_channels"]

    def add_tracker_channel(self, channel_id: int) -> None:
        """Add a tracker channel id to config if it's not already there."""
        if channel_id not in self.config["tracker_channels"]:
            self.config["tracker_channels"].append(channel_id)
            with open("config.yaml", "w") as file:
                yaml.dump(self.config, file)

    def remove_tracker_channel(self, channel_id: int) -> None:
        """Remove a tracker channel id from config if it's present."""
        if channel_id in self.config["tracker_channels"]:
            self.config["tracker_channels"].remove(channel_id)
            with open("config.yaml", "w") as file:
                yaml.dump(self.config, file)