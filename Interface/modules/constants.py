
# Constants for SQLITE
SQLITE_DATABASE_PATH = "../Gateway/gateway.db"
SELECT_DEVICES_QUERY = "SELECT * FROM DEVICE "
SELECT_CONFIG_QUERY  = "SELECT * FROM CONFIG"

# Constants for MQTT
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "interface"
MQTT_PASSWORD  = "interface#2022"

MQTT_TOPIC_GATEWAY_NWK     = "/config/gateway/nwk"
MQTT_TOPIC_GATEWAY_DEV     = "/config/gateway/dev"
