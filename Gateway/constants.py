
# Constants for LORA DEVICE
DEV_EUI_SIZE = 8
DEVICE_IDENTIFIER_SIZE = DEV_EUI_SIZE

# Constants for SQLITE
SQLITE_DATABASE_PATH = "gateway.db"

# Constants for GPS
GPS_START_TIMESTAMP  = 315964800 # January 6, 1980, 00:00:00 (seconds)

# Constants for Packet Encoder Service
PACKET_ENCODER_URL = "http://localhost:8080/"

# Constants for MQTT
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "gateway"
MQTT_PASSWORD  = "gateway#2022"

MQTT_TOPIC_FORWARDER_IN    = "/forwarder/data/in"
MQTT_TOPIC_FORWARDER_OUT   = "/forwarder/data/out"
MQTT_TOPIC_FORWARDER_EUI   = "/forwarder/gateway/eui"
MQTT_TOPIC_FORWARDER_NWK   = "/forwarder/gateway/nwk"

MQTT_TOPIC_TRANSCEIVER_IN  = "/transceiver/data/in"
MQTT_TOPIC_TRANSCEIVER_OUT = "/transceiver/data/out"

MQTT_TOPIC_GATEWAY_EUI     = "/config/gateway/eui"
MQTT_TOPIC_GATEWAY_NWK     = "/config/gateway/nwk"
MQTT_TOPIC_GATEWAY_DEV     = "/config/gateway/dev"

