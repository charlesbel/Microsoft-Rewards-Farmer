import json
import requests
from pathlib import Path

class Telegram:
    def send_to_telegram(message):        
        print("[TELEGRAM]", "Sending telegram message.")
        accountPath = Path(__file__).resolve().parent.parent / "telegram.json"
        if not accountPath.exists():
            accountPath.write_text(
                json.dumps(
                    [{"apitoken": "Your Telegram Token", "chatid": "Your ChatID"}], indent=4
                ),
                encoding="utf-8",
            )
            print("[TELEGRAM]", "Telegram file: telegrama.json created.")
            print("[TELEGRAM]", "Edit with your telegram information and save, then press any key to continue...")
            exit()

        loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))

        for telegraminfo in loadedAccounts:
            apiURL = f'https://api.telegram.org/bot{telegraminfo["apitoken"]}/sendMessage'
    
            try:
                response = requests.post(apiURL, json={'chat_id': telegraminfo["chatid"], 'text': message})
                #print(response.text)
            except Exception as e:
                print(e)