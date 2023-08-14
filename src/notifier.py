import requests

MAX_LENGTHS = {
    "telegram": 4096,
    "discord": 2000,
}


class Notifier:
    def __init__(self, args):
        self.args = {
            key: value
            for key, value in vars(args).items()
            if key in MAX_LENGTHS.keys() and value is not None
        }

    def send(self, message: str):
        for type in self.args:
            if len(message) > MAX_LENGTHS[type]:
                for i in range(0, len(message), MAX_LENGTHS[type]):
                    self.send(message[i : i + MAX_LENGTHS[type]])
                return
            else:
                getattr(self, type)(message)

    def telegram(self, message):
        token, chat_id = self.args["telegram"]
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        requests.post(url, data=data)

    def discord(self, message):
        url = self.args["discord"]
        data = {"username": "Microsoft Rewards Farmer", "content": message}
        requests.post(url, data=data)
