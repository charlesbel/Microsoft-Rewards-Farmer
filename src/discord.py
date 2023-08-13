import json
import logging
from pathlib import Path

import requests


class Discord:
    def check_json():
        accountPath = Path(__file__).resolve().parent.parent / "discord.json"
        if not accountPath.exists():
            accountPath.write_text(
                json.dumps(
                    [{"webhook_url": "Your webhook URL", "bot_username": "Your bot username"}], indent=4
                ),
                encoding="utf-8",
            )
            logging.info("[WEBHOOK] WEBHOOK file: discord.json created.")
            logging.info("[WEBHOOK] Edit with your webhook information and save, then press any key to continue...")
            input()
    def send_to_webhook(message):        
        logging.info("[Discord]", "Sending webhook.")
        accountPath = Path(__file__).resolve().parent.parent / "discord.json"

        loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))

        for webhookinfo in loadedAccounts:
            apiURL = f'{webhookinfo["webhook_url"]}'

            try:
                response = requests.post(apiURL, json={'username': webhookinfo["bot_username"], 'content': message})
            except Exception as e:
                print(e)
