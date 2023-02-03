"""

\x02\x82\xd6\x00[I1\xf9{\x1c\n\x8e{"rxpk":[{"time":"2023-01-11T12:50:05Z","tmms":1357476605,"tmst":1673441405,"chan":0,"rfch":0,"stat":1,"freq":868.1,"brd":0,"rssi":-60,"datr":"SF7BW125","modu":"LORA","codr":"4/5","lsnr":7,"size":23,"data":"AAAAAAAAAAAAr9+I56BcJoHJPcwANmo="}],"stat":{"time":"2023-01-11 12:50:05 UTC","lati":6.152011316947985,"long":1.2591783408612136,"alti":5,"rxnb":51,"rxok":51,"rxfw":7,"ackr":7,"dwnb":79,"txnb":7}}

\x02r\x99\x02[I1\xf9{\x1c\n\x8e

"""






gatewayEUI = '5b4931f97b1c0a8e'
message = {
  "rxpk": [
    {
      "time": '2023-01-11T14:07:04.460Z',
      "tmms": None,
      "tmst": 1673446024,
      "freq": 868300000,
      "chan": None,
      "rfch": 0,
      "stat": 0,
      "modu": 'LORA',
      "datr": 'SF8BW125',
      "codr": '4/5',
      "rssi": -97,
      "lsnr": 12,
      "size": 23,
      "data": 'AAAAAAAAAAAA0/0XJ8q2zGzNTe7u7u4='
    }
  ]
}

import socket

def send_bytes(data, target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (target, port))
    sock.close()


# Example usage
target = "192.168.1.13"
port = 1700
data = b'\x02r\x99\x02[I1\xf9{\x1c\n\x8e'

data = b'\x02\xbe0\x00[I1\xf9{\x1c\n\x8e{"rxpk":[{"time":"2023-01-11T14:42:11Z","tmms":1357483331,"tmst":1673448131,"chan":0,"rfch":0,"stat":1,"freq":868.1,"brd":0,"rssi":-60,"datr":"SF7BW125","modu":"LORA","codr":"4/5","lsnr":7,"size":23,\
	"data":"AAAAAAAAAAAA0/0XJ8q2zGxOzNf49wg="}]}'#\
		#,"stat":{"time":"2023-01-11 12:50:05 UTC","lati":6.152011316947985,"long":1.2591783408612136,"alti":5,"rxnb":51,"rxok":51,"rxfw":7,"ackr":7,"dwnb":79,"txnb":7}\
		#}'
#send_bytes(data, target, port)

gatewayEUI = '5b4931f97b1c0a8e'

import codecs

def sanitizeBuffer(value, encoding):
    if isinstance(value, bytes):
        return value
    return codecs.decode(value, encoding)
data = '5b4931f97b1c0a8e'
encoding = 'hex'

print(bytes([0x02, 0xAF, 0x30, 0x02]) + sanitizeBuffer(data, encoding))



"""

received message: b'\x026\\\x03{"txpk":{"imme":false,"rfch":0,"powe":14,"ant":0,"brd":0,"tmst":1678448131,"freq":868.1,"modu":"LORA","datr":"SF7BW125","codr":"4/5","ipol":true,"size":33,"data":"IGCuoYKKTnOk5tudHlUdFE+2ssXclxSlySbrheF1XuOk"}}'


IGCuoYKKTnOk5tudHlUdFE+2ssXclxSlySbrheF1XuOk

"""

from datetime import datetime

print(datetime.utcnow().isoformat()+'Z',)

now = datetime.now()
print(datetime.fromisoformat(datetime.utcnow().isoformat()))


payload = bytes([0xAF, 0xAE, 0xAD, 0xAC, 0xAB, 0xAA, 0x00, 0x00, 0x44, 0x44])
print(payload)
devEUI = payload[8:].hex()
print(devEUI)
print(hex(15)[2:].zfill(4))