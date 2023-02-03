# Constants for the Semtech UDP protocol
PROTOCOL_VERSION = 2

PKT_PUSH_DATA = 0x00
PKT_PUSH_ACK  = 0x01
PKT_PULL_DATA = 0x02
PKT_PULL_RESP = 0x03
PKT_PULL_ACK  = 0x04
PKT_TX_ACK    = 0x05

PULL_DATA_FREQUENCY = 30 # every 30 seconds

TX_ACK_NO_ERROR = "NONE"
"""Packet has been programmed for downlink"""

DEFAULT_GATEWAY_EUI = "5b4931f97b1c0a8e"

# Constants for MQTT connection
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "forwarder"
MQTT_PASSWORD  = "forwarder#2022"
MQTT_TOPIC_FORWARDER_IN    = "/forwarder/data/in"
MQTT_TOPIC_FORWARDER_OUT   = "/forwarder/data/out"
MQTT_TOPIC_FORWARDER_EUI   = "/forwarder/gateway/eui"
MQTT_TOPIC_FORWARDER_NWK   = "/forwarder/gateway/nwk"


# Constants for Packet Forwarder
QUEUE_MAX_SIZE = 100
