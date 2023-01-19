
# Constants for LORA DEVICE
DEV_EUI_SIZE = 8
DEVICE_IDENTIFIER_SIZE = DEV_EUI_SIZE

# Constants for SQLITE
SQLITE_DATABASE_PATH = "./SQLite/devices.db"

# Constants for Packet Encoder Service
PACKET_ENCODER_URL = "http://localhost:8080/"

# Constants for MQTT
MQTT_BROKER    = "192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "gateway"
MQTT_PASSWORD  = "gateway#2022"
MQTT_TOPIC_FORWARDER_IN    = "/forwarder/data/in"
MQTT_TOPIC_FORWARDER_OUT   = "/forwarder/data/out"
MQTT_TOPIC_TRANSCEIVER_IN  = "/transceiver/data/in"
MQTT_TOPIC_TRANSCEIVER_OUT = "/transceiver/data/out"
MQTT_TOPIC_GATEWAY_ID      = "/forwarder/gateway/id"
