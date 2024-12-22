from uuid import UUID

from src.communication.heartbeat.message_type import MessageType
import logging

# Start logger
logger = logging.getLogger(__name__)
log_console_handler = logging.StreamHandler()
log_file_handler = logging.FileHandler('pyIzzy.log',
                                       mode="a",
                                       encoding="utf-8")
logger.addHandler(log_console_handler)
logger.addHandler(log_file_handler)
formatter = logging.Formatter("{asctime} - {levelname} - {message}",
                              style="{",
                              datefmt="%Y-%m-%d %H:%M")
log_console_handler.setFormatter(formatter)
log_file_handler.setFormatter(formatter)
logger.setLevel(10)
logger.info('Heartbeat Message')


class HeartbeatMessage:
    def __init__(self, message_type=None):
        self.preamble = 0x10
        self.msg_id = [0x69, 0x7A, 0x7A, 0x79, 0x6D, 0x65, 0x73,
                       0x73, 0x61, 0x67, 0x65]  # 'izzymessage'
        self.msg_length = 46
        self.sender_id = None
        self.receiver_id = None
        self.message_type = message_type
        self.data = None

    def set_data(self, data):
        self.data = data
        if self.data is not None:
            self.msg_length += len(self.data)

    def process_packet(self, raw_data):
        self.preamble = raw_data[0]
        self.msg_id = raw_data[1:12]
        if len(raw_data) == int(raw_data[12]):
            self.msg_length = int(raw_data[12])
            self.sender_id = UUID(bytes=raw_data[13:29])
            self.receiver_id = UUID(bytes=raw_data[29:45])
            self.message_type = raw_data[45]
            if len(raw_data) > 46:
                self.data = raw_data[46:len(raw_data)]
            else:
                self.data = None
            return True
        else:
            return False

    def get_message(self):
        message = bytearray()
        message.append(self.preamble)

        if self.msg_id is not None:
            for byte in self.msg_id:
                message.append(byte)
        else:
            for i in range(0, 11):
                message.append(0x00)

        message.extend(self.msg_length.to_bytes(1, "big"))

        if self.sender_id is not None:
            for byte in self.sender_id:
                message.append(byte)
        else:
            for i in range(0, 16):
                message.append(0x00)

        if self.receiver_id is not None:
            for byte in self.receiver_id:
                message.append(byte)
        else:
            for i in range(0, 16):
                message.append(0x00)

        message.append(self.message_type)

        if self.data is not None:
            for byte in self.data:
                message.append(byte)

        return message
