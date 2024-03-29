
# Constants for MQTT connection
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "transceiver"
MQTT_PASSWORD  = "transceiver#2022"
MQTT_TOPIC_TRANSCEIVER_IN  = "/transceiver/data/in"
MQTT_TOPIC_TRANSCEIVER_OUT = "/transceiver/data/out"
MQTT_TOPIC_TRANSCEIVER_CONF= "/transceiver/data/conf"

# 
TRANSCEIVER_DATA_MIN_SIZE = 8
CONFIG_FILE_PATH = "../Gateway/gateway.json"


# Constants for Dorji configuration
DORJI_SYNC_WORD = 0xAF
DORJI_ID_CODE = 0x00
DORJI_HEADER = 0xAF
DORJI_LENGTH = 0x0E
DORJI_END_CODE_CR = 0x0D
DORJI_END_CODE_LF = 0x0A

DORJI_CMD_SEND = 0x80
DORJI_CMD_RESPONSE = 0x00

DORJI_CMD_WRITE = 0x01
DORJI_CMD_READ = 0x02
DORJI_CMD_STANDARD = 0x03
DORJI_CMD_CENTRAL = 0x04
DORJI_CMD_NODE = 0x05

DORJI_CMD_DATA_BAUDRATE = 0x04
DORJI_CMD_DATA_PARITY = 0x00
DORJI_CMD_DATA_MODE = 0x00
DORJI_CMD_DATA_NODE_ID = 0x00
DORJI_CMD_DATA_NET_ID = 0x06
DORJI_CMD_DATA_POWER = 0x07
DORJI_CMD_DATA_BREATH = 0x00
DORJI_CMD_DATA_WAKE_TIME = 0x04

DORJI_CMD_DATA_FREQUENCY_DIVIDER = 61.035
DORJI_CMD_DATA_BANDWITH_125K = 0x07
DORJI_CMD_DATA_BANDWITH_250K = 0x08