import requests
from .message_api_dto import MessageApiDto

class MessageHandler:
    def __init__(self, token):
        self.token = token

    def send_message(self, options: MessageApiDto) -> bool:
        url = "https://api.bitmoro.com/message/api"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "number": options.number,
            "message": options.message,
            "senderId": options.sender_id,
            "timer": options.timer.isoformat() if options.timer else None
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code >= 400:
            raise Exception(response.text)
        return True