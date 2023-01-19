import os, json
from constants import *

class Handler():

    def __init__(self, gateway_id : str):
        self.__mapping__    = {}
        self._token_x       = bytes([0x00, 0x00])
        self._token_y       = bytes([0x00, 0x00])
        self._token_z       = bytes([0x00, 0x00])
        self._gateway_id    = bytes.fromhex(gateway_id)

    def set_gateway_id(self, gateway_id : str):
        self._gateway_id    = bytes.fromhex(gateway_id)
    
    def validate_token_x(self, data : bytes) -> bytes:
        token = data[1:3]
        if self._token_x == token:
            return True
        return False
    
    def validate_token_y(self, data : bytes) -> bytes:
        token = data[1:3]
        if self._token_y == token:
            return True
        return False

    def save_token_z(self, data : bytes) -> bytes:
        self._token_z = data[1:3]
        return self._token_z

    def push_data(self, data : str) -> bytes:
        data = bytes(data, encoding='utf8')
        self._token_x = os.urandom(2)
        print("PUSH_DATA Ready")
        return b''.join([bytes([PROTOCOL_VERSION]), self._token_x, bytes([PKT_PUSH_DATA]), self._gateway_id, data])

    def push_ack(self, data : bytes) -> bytes:
        print("PUSH_ACK Received")
        return self.validate_token_x(data)

    def pull_data(self) -> bytes:
        self._token_y = os.urandom(2)
        print("PULL_DATA Ready")
        return b''.join([bytes([PROTOCOL_VERSION]), self._token_y, bytes([PKT_PULL_DATA]), self._gateway_id])

    def pull_ack(self, data : bytes) -> bytes:
        print("PULL_ACK Received")
        return self.validate_token_y(data)

    def pull_resp(self, data : bytes) -> bytes:
        print("PULL_RESP Received")
        return self.save_token_z(data)

    def tx_ack(self, token_z : bytes) -> bytes:
        data =  { "txpk_ack":
                    {
                        "error":TX_ACK_NO_ERROR
                    }
                }
        data = bytes(json.dumps(data), encoding='utf-8')
        print("TX_ACK Ready")
        return b''.join([bytes([PROTOCOL_VERSION]), token_z, bytes([PKT_TX_ACK]), self._gateway_id, data])


    




