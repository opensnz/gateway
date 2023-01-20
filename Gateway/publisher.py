
import paho.mqtt.client as mqtt
import json
from constants import *

mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")

DevEUI = "b53fcaaa8725fe1b"

#payload = "68100001020304050681319012002C601300002C150515002C330303033556353700043600303016111119200012005716"
payload = "6810AAAAAAAAAAAAAA81319012002C601300002C150515002C33030303355635370004360030301611111920001200E816"


mqtt_client.username_pw_set("transceiver","transceiver#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":DevEUI+payload}))
