
# Constants for SQLITE
SQLITE_DATABASE_PATH = "../Gateway/gateway.db"
SELECT_DEVICES_QUERY = "SELECT * FROM DEVICE "

# Constants for web app
WEB_APP_BIND  = "0.0.0.0"
WEB_APP_PORT  = 86  # must be 80 in final version

# Constants for MQTT
MQTT_BROKER    = "localhost"#"192.168.1.241"
MQTT_PORT      = 1883
MQTT_USERNAME  = "interface"
MQTT_PASSWORD  = "interface#2022"

MQTT_TOPIC_GATEWAY_NWK     = "/config/gateway/nwk"
MQTT_TOPIC_GATEWAY_DEV     = "/config/gateway/dev"

CONFIG_FILE_PATH = "../Gateway/gateway.json"