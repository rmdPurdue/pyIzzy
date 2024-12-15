class Server():
    def __init__(self, id=0):
        self.id = id
        self.ip_address = None
        self.last_contact = None

    def get_id(self):
        return self.id

    def get_ip_address(self):
        return self.ip_address

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_last_contact(self):
        return self.last_contact

    def set_last_contact(self, last_contact):
        self.last_contact = last_contact

