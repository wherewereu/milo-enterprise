#!/usr/bin/env python3
"""
Agent Discord poster — posts as individual agent bots.
Usage: python3 ~/.openclaw/discord-post.py <agent_name> <message>
       python3 ~/.openclaw/discord-post.py <agent_name> <message> --reply-to <message_id>
       python3 ~/.openclaw/discord-post.py <agent_name> <message> --channel <channel_id>
       python3 ~/.openclaw/discord-post.py <agent_name> <message> --react-to <message_id>
"""
import sys, json, http.client

import os; config = json.load(open(os.environ.get('AGENT_TOKENS_PATH', os.path.expanduser('~/.openclaw/agent-bot-tokens.json'))))

agent = sys.argv[1]
message = sys.argv[2]
reply_to = None
channel_id = config['round_table_channel']  # default to round table

if '--reply-to' in sys.argv:
    idx = sys.argv.index('--reply-to')
    reply_to = sys.argv[idx + 1]

if '--channel' in sys.argv:
    idx = sys.argv.index('--channel')
    channel_id = sys.argv[idx + 1]

token = config['bots'].get(agent)
if not token:
    print(f"Unknown agent: {agent}")
    sys.exit(1)

payload = {"content": message}
if reply_to:
    payload["message_reference"] = {"message_id": reply_to}

conn = http.client.HTTPSConnection("discord.com")
conn.request(
    "POST",
    f"/api/v10/channels/{channel_id}/messages",
    body=json.dumps(payload),
    headers={
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)"
    }
)
resp = conn.getresponse()
data = json.loads(resp.read())
if resp.status == 200:
    print(f"Posted as {agent} to {channel_id}, message_id: {data['id']}")
else:
    print(f"Failed: {resp.status} {data}")

# Handle reactions
if '--react-to' in sys.argv:
    idx = sys.argv.index('--react-to')
    react_to_msg_id = sys.argv[idx + 1]
    
    # Use white checkmark emoji
    emoji = "✅"
    encoded_emoji = "%E2%9C%85"
    
    conn.request(
        "PUT",
        f"/api/v10/channels/{channel_id}/messages/{react_to_msg_id}/reactions/{encoded_emoji}/@me",
        body=None,
        headers={
            "Authorization": f"Bot {token}",
            "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)"
        }
    )
    react_resp = conn.getresponse()
    if react_resp.status == 204:
        print(f"Reacted with ✅ to message {react_to_msg_id}")
    else:
        print(f"React failed: {react_resp.status}")
