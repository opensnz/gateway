
import paho.mqtt.client as mqtt
from constants import *
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD2 as BOARD


class Transceiver():


    def __init__(self):
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")


    def __setup__(self):
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        while True:
            print("Transceiver Waiting for data...")
            # Read incoming data
            payload = ""
            # Publish data
            self.__mqtt_client.publish(topic=MQTT_TOPIC_TRANSCEIVER_OUT, payload=payload)
        

    def main(self) -> None:
        """run transceiver forever"""
        try :
            print("Transceiver setting...")
            self.__setup__()
            print("Transceiver running...")
            """2 Threads run forever and concurrently"""
            self.__mqtt_client.loop_start()
            self.__loop__()
            
        except Exception as e:
            print("Exception in the main Thread:", e)
            self.__mqtt_client.loop_stop()
            raise Exception("Raised exception to relaunch Transceiver Service")


    def __mqtt_on_message__(self,  client : mqtt.Client, userdata, message:mqtt.MQTTMessage):
        print("MQTT_Message received")


    def __mqtt_on_connect__(self, client : mqtt.Client, userdata, flags, rc):
        print("MQTT_Client connected")
        client.subscribe(MQTT_TOPIC_TRANSCEIVER_IN)


    def __mqtt_on_disconnect__(self, client : mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")




if __name__ == "__main__":
    transceiver = Transceiver()
    transceiver.main()

