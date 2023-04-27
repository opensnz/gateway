from constants import *




def dorji_cmd_config(frequency : int, bandwith : int, spreading_factor : int) -> bytes:
    config = bytes([DORJI_SYNC_WORD, DORJI_SYNC_WORD, DORJI_ID_CODE, DORJI_ID_CODE, DORJI_HEADER, 
                    DORJI_CMD_SEND, DORJI_CMD_WRITE, DORJI_LENGTH])
    
    data = dorji_cmd_data(frequency, bandwith, spreading_factor)

    if len(data) != DORJI_LENGTH:
        return None

    config = config + data
    config = config + bytes([dorji_cmd_crc(config)])
    config = config + bytes([DORJI_END_CODE_CR, DORJI_END_CODE_LF])
    return config



def dorji_cmd_crc(command : bytes) -> int:
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

