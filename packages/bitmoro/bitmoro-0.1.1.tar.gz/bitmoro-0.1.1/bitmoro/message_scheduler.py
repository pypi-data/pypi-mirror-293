import threading
from datetime import datetime
from .message_handler import MessageHandler
from .message_api_dto import MessageApiDto

class MessageScheduler:
    def __init__(self, token):
        self.sms = MessageHandler(token)

    def schedule_sms(self, message, number, timer, sender_id=None):
        if timer < datetime.now():
            raise ValueError("Scheduled time must be in the future.")
        
        time_difference = (timer - datetime.now()).total_seconds()

        def send_task():
            try:
                send_body = MessageApiDto(message=message, number=number, sender_id=sender_id, timer=timer)
                self.sms.send_message(send_body)
                print("Message sent successfully at the scheduled time.")
            except Exception as e:
                print(f"Failed to send the scheduled message: {str(e)}")

        threading.Timer(time_difference, send_task).start()