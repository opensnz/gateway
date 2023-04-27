# Constants for the Semtech UDP protocol
PROTOCOL_VERSION = 2

PKT_PUSH_DATA = 0x00
PKT_PUSH_ACK  = 0x01
PKT_PULL_DATA = 0x02
PKT_PULL_RESP = 0x03
PKT_PULL_ACK  = 0x04
PKT_TX_ACK    = 0x05


# Constants for MQTT connection
MQTT_BROKER    = "localhost"
MQTT_PORT      = 1883
MQTT_USERNAME  = "forwarder"
MQTT_PASSWORD  = "forwarder#2022"
MQTT_TOPIC_FORWARDER_IN    = "/forwarder/data/in"
MQTT_TOPIC_FORWARDER_OUT   = "/forwarder/data/out"
MQTT_TOPIC_FORWARDER_CONF  = "/forwarder/data/conf"


# Constants for Packet Forwarder
CONFIG_FILE_PATH = "../Gateway/gateway.json"
