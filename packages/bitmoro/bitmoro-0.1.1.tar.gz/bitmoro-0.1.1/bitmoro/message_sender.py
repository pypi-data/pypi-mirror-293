from .message_handler import MessageHandler
from .message_api_dto import MessageApiDto

class MessageSenderError(Exception):
    pass

class MessageSender:
    def __init__(self, token):
        self.sms = MessageHandler(token)

    def send_sms(self, message, number, sender_id=None) -> bool:
        send_body = MessageApiDto(message=message, number=number, sender_id=sender_id)
        try:
            self.sms.send_message(send_body)
            return True
        except Exception as e:
            raise MessageSenderError(str(e))