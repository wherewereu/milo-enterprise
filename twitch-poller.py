#!/usr/bin/env python3
import requests
import json
import os
import subprocess
from datetime import datetime

CLIENT_ID = "itebr7xehfmt443fdlw9iqsxdvjn5e"
CLIENT_SECRET = "to9enay7npjou6xby16rpulb3oyjap"
BROADCASTER_LOGIN = "zackrawrr"
STATE_FILE = os.path.expanduser("~/.openclaw/twitch-state.json")

def get_token():
    r = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    return r.json()["access_token"]

def is_live(token):
    r = requests.get("https://api.twitch.tv/helix/streams",
        params={"user_login": BROADCASTER_LOGIN},
        headers={"Client-ID": CLIENT_ID, "Authorization": f"Bearer {token}"}
    )
    data = r.json().get("data", [])
    if data:
        return True, data[0].get("title", "")
    return False, ""

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"was_live": False, "last_notified": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_imessage(msg):
    cmd = ["osascript", "-e", f'tell application "Messages" to send "{msg}" to buddy "+16293959407"']
    subprocess.run(cmd)

def main():
    state = load_state()
    try:
        token = get_token()
        live, title = is_live(token)

        if live and not state["was_live"]:
            msg = f"Asmongold is live! {title} twitch.tv/zackrawrr"
            send_imessage(msg)
            state["was_live"] = True
            state["last_notified"] = datetime.now().isoformat()
        elif not live and state["was_live"]:
            state["was_live"] = False

        save_state(state)
    except Exception as e:
        with open(os.path.expanduser("~/.openclaw/logs/twitch-poller.log"), "a") as f:
            f.write(f"{datetime.now()} ERROR: {e}\n")

if __name__ == "__main__":
    main()
