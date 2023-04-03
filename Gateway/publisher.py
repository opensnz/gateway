
import paho.mqtt.client as mqtt
import json
from constants import *

mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")

DevEUI = "c2e1bce5f95abcae"
#DevEUI = "A840415411822622"
DevEUI = "f8e420ac9753b6a2"
#payload = "68100001020304050681319012002C601300002C150515002C330303033556353700043600303016111119200012005716"
payload = "4e4e202d31372e39302031392e363720342e30382038300a"


mqtt_client.username_pw_set("transceiver","transceiver#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":DevEUI+payload}))
