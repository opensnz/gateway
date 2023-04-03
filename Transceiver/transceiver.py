
import paho.mqtt.client as mqtt
import base64, json, time
import threading
import serial
from constants import *
from dorji import *


class Transceiver():


    def __init__(self):
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")


    def __setup__(self):
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # Open serial port with baud rate
        self.__ser = serial.Serial (port='/dev/ttyAMA0',
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=None) 


    def __loop__(self):
        while True:
            print("Transceiver Waiting for data...")
            # Read incoming data
            self.__ser.flushInput()
            data =  self.__ser.read()
            time.sleep(0.01)
            while  self.__ser.in_waiting:
                data = data +  self.__ser.read( self.__ser.in_waiting)
                if self.__ser.in_waiting == 0:
                    time.sleep(0.01)
            payload = data[1:]
            print(payload)
            threading.Timer(0, self.__one_shot_task__, args=(payload,)).start()


    def __one_shot_task__(self, payload:bytes):
        try:
            self.__mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":payload.hex()}))
        except:
            pass


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

