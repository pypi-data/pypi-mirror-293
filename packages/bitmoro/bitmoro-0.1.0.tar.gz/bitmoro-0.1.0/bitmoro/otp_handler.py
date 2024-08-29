import threading
import random
from datetime import datetime
from .message_handler import MessageHandler
from .message_api_dto import MessageApiDto
from .message_sender import MessageSenderError

class OtpHandler:
    valid_otp = {}
    exp = 40  # seconds

    def __init__(self, token, exp=40, otp_length=10):
        self.token = token
        self.otp_length = otp_length
        self.sms = MessageHandler(token)
        OtpHandler.exp = exp

    def send_otp_message(self, number, sender_id=None) -> bool:
        otp = self.generate_otp(self.otp_length)
        message = f"Your OTP code is {otp}"

        send_body = MessageApiDto(message=message, number=[number], sender_id=sender_id)
        try:
            self.sms.send_message(send_body)
            self.register_otp(number, otp)
            return True
        except Exception as e:
            raise MessageSenderError(str(e))

    def register_otp(self, number, otp):
        if number in OtpHandler.valid_otp:
            existing_otp = OtpHandler.valid_otp[number]
            time_left = (datetime.now() - existing_otp['time']).total_seconds()
            raise Exception(f"You can only request OTP after {time_left} second(s)")

        otp_body = {
            "otp": otp,
            "time": datetime.now()
        }
        OtpHandler.valid_otp[number] = otp_body
        self.clear_otp(number)

    def clear_otp(self, number):
        def clear_task():
            if number in OtpHandler.valid_otp:
                del OtpHandler.valid_otp[number]

        threading.Timer(OtpHandler.exp, clear_task).start()

    def generate_otp(self, length) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def verify_otp(self, number, otp) -> bool:
        if number not in OtpHandler.valid_otp:
            raise Exception(f"No OTP found for number {number}")

        registered_otp = OtpHandler.valid_otp[number]
        return registered_otp['otp'] == otp