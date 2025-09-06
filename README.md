# Hypixel Ban Tracker

A Discord bot that provides real-time monitoring and reporting of bans on the Hypixel Minecraft server, helping administrators and players stay informed about server ban activity.

## Features

- **Real-time Monitoring**: Tracks watchdog and staff bans every 30 seconds
- **Automated Updates**: Sends live ban statistics to subscribed Discord channels
- **Clean Interface**: Uses Discord embeds for professional presentation
- **Easy Management**: Simple commands to subscribe/unsubscribe channels
- **Scalable Architecture**: Handles multiple servers efficiently

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kWAYTV/hypixel-ban-tracker-bot.git
cd hypixel-ban-tracker-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the bot:

```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your bot token and settings
```

4. Run the bot:

```bash
python main.py
```

## Configuration

Edit `config.yaml` with the following settings:

- `bot_token`: Your Discord bot token
- `dev_guild_id`: Guild ID for development/testing
- `log_file`: Path for log file output
- `update_batch_size`: Servers to update per batch (default: 5)
- `batch_delay`: Delay between batches in seconds (default: 1.0)
- `max_concurrent_updates`: Maximum concurrent server updates (default: 3)

## Commands

| Command        | Description                             | Permissions   |
| -------------- | --------------------------------------- | ------------- |
| `/ping`        | Test bot connectivity and latency       | Administrator |
| `/broadcast`   | Subscribe channel to ban updates        | Administrator |
| `/unbroadcast` | Unsubscribe and clean up ban panel      | Administrator |
| `/info`        | Display bot statistics                  | Administrator |
| `.sync`        | Sync slash commands (optional guild ID) | Administrator |

## Usage

1. Invite the bot to your Discord server
2. Use `/broadcast` in the desired channel to start receiving ban updates
3. The bot will automatically update live ban statistics every 30 seconds
4. Use `/unbroadcast` to stop updates and clean up messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial project and is not affiliated with, maintained, sponsored, or endorsed by Hypixel, Mojang/Microsoft, or Discord. Use responsibly and in accordance with all applicable terms of service.
