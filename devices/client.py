class Izzy():
    def __init__(self, id):
        self.mother = None
        self.id = id
        self.ip_address = None
        self.status = heartbeat.izzy_status.MISSING

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

    def get_mother(self):
        return self.mother

    def set_mother(self, mother):
        self.mother = mother

