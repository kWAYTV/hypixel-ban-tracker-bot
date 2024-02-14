# 🏰 HypixelBanChecker 🛡️

Welcome to the HypixelBanChecker, a discord bot that actively monitors and reports bans on the Hypixel Minecraft server. The bot is intended to assist administrators and players by providing real-time ban data fetched directly from the Hypixel API. It's designed to work seamlessly with your existing discord channels.

## 📖 About

HypixelBanChecker tracks watchdog (automatic) and staff (manual) bans on the Hypixel Minecraft server. The bot is easy to set up and use, and it offers real-time updates on the ban status of players on the Hypixel server.

## 🚀 Features

1. **Real-time Updates** - The bot checks the ban status every 0.1 seconds.
2. **Easy to Use Commands** - Subscribing or unsubscribing a channel from the ban updates is as simple as running a command.
3. **Embeds for Better Visualization** - The bot uses Discord Embeds for a better visual presentation of ban data.

## 🛠️ Setup

1. Clone the repository & install the requirements.
2. Update the `config.yaml` file with your discord token and the channel IDs where you want the bot to send updates.
3. Run the bot!

```bash
python main.py
```

## 🖐️ Commands

- `/ping` - Tests the bot.
- `/broadcast` - Subscribes the channel to the Ban Tracker.
- `/log_channel` - Sets the channel where the bot will send logs.
- `.sync` - Syncs the bot commands with the server. (You can provide a Guild ID to sync a specific server only)

## ⚠️ Disclaimer

This is a Proof of Concept (PoC) project. It is not officially affiliated with, maintained, sponsored or endorsed by Hypixel or Mojang/Microsoft. Use this tool responsibly and respect the Hypixel server rules and terms.
