class MessageApiDto:
    def __init__(self, number=None, message=None, sender_id=None, timer=None):
        self.number = number if number else []
        self.message = message
        self.sender_id = sender_id
        self.timer = timer