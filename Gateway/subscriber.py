import paho.mqtt.client as mqtt
from constants import *

mqtt_client = mqtt.Client(transport="tcp",client_id="subscriber")

def mqtt_on_message(client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
    print("MQTT_Message received")
    try:
        payload = eval(message.payload)
        print(payload)
    except Exception as e:
        print(e)
        pass
    finally:
        pass


def mqtt_on_connect(client:mqtt.Client, userdata, flags, rc):
    print("MQTT_Client connected")
    client.subscribe(MQTT_TOPIC_FORWARDER_OUT)


def mqtt_on_disconnect(client:mqtt.Client, userdata, rc):
    print("MQTT_Client disconnected")




mqtt_client.username_pw_set("transceiver","transceiver#2022")
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_disconnect = mqtt_on_disconnect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

mqtt_client.loop_forever()
