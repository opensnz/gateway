
import paho.mqtt.client as mqtt
import json
from constants import *




mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")
configuring = False


mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect("192.168.4.74", MQTT_PORT)


payload = "AABBCCDD"

mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":"c2e1bce5f95abcae"+payload}))