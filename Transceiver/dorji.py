import serial, time
from constants import *


ser = serial.Serial (port='COM3',
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=None) 




def dorji_command(frequency : int, bandwith : int, spreading_factor : int) -> bytes:
    config = bytes([DORJI_SYNC_WORD, DORJI_SYNC_WORD, DORJI_ID_CODE, DORJI_ID_CODE, DORJI_HEADER, 
                    DORJI_CMD_SEND, DORJI_CMD_WRITE, DORJI_LENGTH])
    
    data = dorji_cmd_data(frequency, bandwith, spreading_factor)

    if len(data) != DORJI_LENGTH:
        return None

    config = config + data
    config = config + bytes([dorji_crc(config)])
    config = config + bytes([DORJI_END_CODE_CR, DORJI_END_CODE_LF])
    return config



def dorji_crc(command : bytes) -> int:
    return sum(command) % 256


def dorji_cmd_data(frequency : int, bandwith : int, spreading_factor : int) -> bytes:
    data = bytes([DORJI_CMD_DATA_BAUDRATE, DORJI_CMD_DATA_PARITY])
    freq = int(frequency / DORJI_CMD_DATA_FREQUENCY_DIVIDER)
    data = data + freq.to_bytes(3, 'big')
    data = data + bytes([spreading_factor, DORJI_CMD_DATA_MODE])
    if bandwith == 125000:
        data = data + bytes([DORJI_CMD_DATA_BANDWITH_125K])
    elif bandwith == 250000:
        data = data + bytes([DORJI_CMD_DATA_BANDWITH_250K])
    
    data = data + bytes([DORJI_CMD_DATA_NODE_ID, DORJI_CMD_DATA_NODE_ID, DORJI_CMD_DATA_NET_ID, 
                         DORJI_CMD_DATA_POWER,
                         DORJI_CMD_DATA_BREATH, DORJI_CMD_DATA_WAKE_TIME])
    return data


print(dorji_crc(bytes([0x01, 0x02])))



command = dorji_command(868700000, 250000, 8)
print(command)
ser.write(command)

response = ser.read()
time.sleep(0.1)
while ser.in_waiting:
    response = response + ser.read(ser.in_waiting)
    time.sleep(0.1)

print(response)