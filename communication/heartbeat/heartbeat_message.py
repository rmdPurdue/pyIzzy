from communication.heartbeat.message_type import MessageType


class HeartbeatMessage:
    def __init__(self, message_type=MessageType.HEARTBEAT):
        self.preamble = 0x10
        self.msg_id = {0x68, 0x7A, 0x7A, 0x79, 0x6D, 0x65, 0x73,
                       0x73, 0x61, 0x67, 0x65} # 'izzymesage'
        self.msg_length = None
        self.sender_id = None
        self.receiver_id = None
        self.message_type = message_type
        self.data = None

    def get_sender_id(self):
        return self.sender_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id

    def get_receiver_id(self):
        return self.receiver_id

    def set_receiver_id(self, receiver_id):
        self.receiver_id = receiver_id

    def get_message_type(self):
        return self.message_type

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.length = 47 + data.length

    def process_packet(self, raw_data):
        if(raw_data[0] == self.preamble):
            if(raw_data[1:12] == self.msg_id):
                if(raw_data.length == int.from_bytes(raw_data[12:14], "big")):
                    self.msg_length = int.from_bytes(raw_data[12:14], "big")
                    self.sender_id = int.from_bytes(raw_data[14:30], "big")
                    self.receiver_id = int.from_bytes(raw_data[30:46], "big")
                    self.message_type = raw_data[46]
                    if(raw_data.length > 47):
                        self.data = raw_data[47:raw_data.length]
                    else:
                        self.data = None
                    return True
                else: return False
            else: return False
        else: return False

    def get_message(self):
