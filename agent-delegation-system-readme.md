# Agent Delegation System

> Discord bot and token setup for Milo Enterprise agents.

## Discord Setup

Each agent requires its own Discord bot token. Tokens are stored in `~/.openclaw/agent-bot-tokens.json`.

### Creating Bot Tokens

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application for each agent
3. Under **Bot**, click **Reset Token** to get the bot token
4. Enable necessary intents (Guilds, Guild Messages, Message Content)
5. Invite each bot to your server with appropriate permissions

### Token Format

```json
{
  "milo": "YOUR_BOT_TOKEN_HERE",
  "archie": "YOUR_BOT_TOKEN_HERE",
  "atro": "YOUR_BOT_TOKEN_HERE",
  "eris": "YOUR_BOT_TOKEN_HERE",
  "hephaestus": "YOUR_BOT_TOKEN_HERE",
  "heracles": "YOUR_BOT_TOKEN_HERE",
  "mercury": "YOUR_BOT_TOKEN_HERE",
  "themis": "YOUR_BOT_TOKEN_HERE"
}
```

### Channel IDs

Refer to `README.md` for the full list of Discord channel IDs used by the system.

---

*This file covers Discord-specific setup. For full system installation, see `README.md`.*
