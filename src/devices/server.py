from datetime import datetime


class Server:
    def __init__(self):
        self.status = None
        self.my_id = None
        self.ip_address = None
        self.last_contact = None

    def set_last_contact(self):
        self.last_contact = datetime.now()

