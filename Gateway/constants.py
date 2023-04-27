
# Constants for LORA DEVICE
DEV_EUI_SIZE = 8
DEVICE_IDENTIFIER_SIZE = DEV_EUI_SIZE

# Constants for config file
CONFIG_FILE_PATH = "gateway.json"

# Constants for SQLITE
SQLITE_DATABASE_PATH = "gateway.db"

# Constants for GPS
GPS_START_TIMESTAMP  = 315964800 # January 6, 1980, 00:00:00 (seconds)

JOIN_REQUEST_FREQUENCY = 86400  # 1 day = 86400s 

# Constants for Packet Encoder Service
PACKET_ENCODER_URL = "http://localhost:8080/"

GATEWAY_INTERNET_CHECKING_FREQUENCY = 1

# Constants for MQTT
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "gateway"
MQTT_PASSWORD  = "gateway#2022"

MQTT_TOPIC_FORWARDER_IN    = "/forwarder/data/in"
MQTT_TOPIC_FORWARDER_OUT   = "/forwarder/data/out"
MQTT_TOPIC_FORWARDER_CONF  = "/forwarder/data/conf"

MQTT_TOPIC_TRANSCEIVER_IN  = "/transceiver/data/in"
MQTT_TOPIC_TRANSCEIVER_OUT = "/transceiver/data/out"
MQTT_TOPIC_TRANSCEIVER_CONF= "/transceiver/data/conf"

MQTT_TOPIC_GATEWAY_NWK     = "/config/gateway/nwk"
MQTT_TOPIC_GATEWAY_DEV     = "/config/gateway/dev"


MQTT_TOPIC_GATEWAY_OFFLINE = "/config/gateway/offline"
MQTT_TOPIC_GATEWAY_STATUS  = "/config/gateway/online"
