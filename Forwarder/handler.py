import os, json
from datetime import datetime
from constants import *

class Handler():

    def __init__(self, gateway_id : str):
        self._token_x       = bytes([0x00, 0x00])
        self._token_y       = bytes([0x00, 0x00])
        self._token_z       = bytes([0x00, 0x00])
        self._gateway_id    = bytes.fromhex(gateway_id)
        self.gateway_lon    = 0
        self.gateway_lat    = 0
        self.gateway_alt    = 0
        self.stat_timestamp = 0
        self.stat_interval  = 0
        self.alive_interval = 0
        self.lora_rxnb      = 0
        self.lora_txnb      = 0
        self.pkt__rxnb      = 0
        self.pkt__txnb      = 0
        self.pkt_acknb      = 0

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
        self.lora_rxnb = self.lora_rxnb + 1
        self.pkt__txnb = self.pkt__txnb + 1
        return b''.join([bytes([PROTOCOL_VERSION]), self._token_x, bytes([PKT_PUSH_DATA]), self._gateway_id, data])

    def push_ack(self, data : bytes) -> bytes:
        self.pkt_acknb = self.pkt_acknb + 1
        self.pkt__rxnb = self.pkt__rxnb + 1
        return self.validate_token_x(data)

    def pull_data(self) -> bytes:
        self._token_y = os.urandom(2)
        self.pkt__txnb = self.pkt__txnb + 1
        return b''.join([bytes([PROTOCOL_VERSION]), self._token_y, bytes([PKT_PULL_DATA]), self._gateway_id])

    def pull_ack(self, data : bytes) -> bytes:
        self.pkt_acknb = self.pkt_acknb + 1
        self.pkt__rxnb = self.pkt__rxnb + 1
        return self.validate_token_y(data)

    def pull_resp(self, data : bytes) -> bytes:
        self.pkt__rxnb = self.pkt__rxnb + 1
        return self.save_token_z(data)

    def tx_ack(self, token_z : bytes) -> bytes:
        data =  { "txpk_ack":
                    {
                        "error":TX_ACK_NO_ERROR
                    }
                }
        data = bytes(json.dumps(data), encoding='utf-8')
        self.lora_txnb = self.lora_txnb + 1
        return b''.join([bytes([PROTOCOL_VERSION]), token_z, bytes([PKT_TX_ACK]), self._gateway_id, data])



    def push_stat(self) -> bytes:
        ackr = 0.00
        if self.pkt__txnb > 0:
            ackr = round((100.0 * self.pkt_acknb)/(self.pkt__txnb), 2)
        data = {"stat":
                    {
                        "time":str(datetime.utcnow()).split(".")[0]+' GMT',
                        "lati":round(self.gateway_lon, 5),
                        "long":round(self.gateway_lon, 5),
                        "alti":int(self.gateway_alt),
                        "rxnb":self.lora_rxnb,
                        "rxok":self.lora_rxnb,
                        "rxfw":self.lora_txnb,
                        "ackr":ackr,
                        "dwnb":self.pkt__rxnb,
                        "txnb":self.pkt__txnb
                    }
                }
        data = self.push_data(json.dumps(data))
        self.lora_rxnb = self.lora_rxnb - 1
        return data
    




