import urllib.request
import time
import paho.mqtt.client as mqtt
import json
from constants import *
from database import Database
import threading



class Offline():


    def __init__(self):
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="offline")
        self._db = Database()
        self.__status = False # connection status (True -> online & False -> offline)


    def __setup__(self):
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        while True:
            is_connected = self.__check_internet__()
            if is_connected and self.__status != is_connected :
                packet = self.__get_offline_packet__()
                if packet is not None :
                    self.__publish__(MQTT_TOPIC_FORWARDER_IN, packet)

            if self.__status != is_connected:
                self.__status = is_connected
                self.__publish__(MQTT_TOPIC_GATEWAY_STATUS, {"status" : self.__status})
                if self.__status :
                    packet = self.__get_offline_packet__()
                    if packet is not None :
                        self.__publish__(MQTT_TOPIC_FORWARDER_IN, packet)
                        
            time.sleep(GATEWAY_INTERNET_CHECKING_FREQUENCY)
    
    
    def main(self) -> None:
        """run offline system forever"""
        try :
            print("Offline System setting...")
            self.__setup__()
            print("Offline System running...")
            """2 Threads run forever and concurrently"""
            self.__mqtt_client.loop_start()
            self.__loop__()
            
        except Exception as e:
            print("Exception in the main Thread:", e)
            self.__mqtt_client.loop_stop()
            raise Exception("Raised exception to relaunch Offline Service")
        

    def __check_internet__(self):
        try :
            urllib.request.urlopen('https://www.google.com', timeout=1)
            return True
        except :
            return False


    def __mqtt_on_message__(self,  client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        print("MQTT_Message received")
        threading.Timer(0, self.__one_shot_task__, args=(message,)).start()


    def __mqtt_on_connect__(self, client:mqtt.Client, userdata, flags, rc):
        print("MQTT_Client connected")
        client.subscribe(MQTT_TOPIC_GATEWAY_OFFLINE)


    def __mqtt_on_disconnect__(self, client:mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")

    def __one_shot_task__(self, message:mqtt.MQTTMessage):
        topic = message.topic
        payload = json.loads((b''+message.payload).decode())
        if topic == MQTT_TOPIC_GATEWAY_OFFLINE:
            self._db.open()
            self._db.insert_device_data(payload["DevEUI"], json.dumps(payload["Packet"]))
            self._db.close()

    def __get_offline_packet__(self) -> dict: 
        packet = self.__generic_packet__()
        offline_packet = []
        self._db.open()
        offline_data = self._db.get_all_data()
        self._db.delete_all_data()
        self._db.close()
        for data in offline_data:
            offline_packet.append(json.loads(data["Packet"]))
        if len(offline_packet) == 0:
            return None
        packet["rxpk"] = offline_packet
        return packet


    def __generic_packet__(self) -> dict:
        packet = {
            "rxpk": [
            ]
        }
        return packet
    
    def __publish__(self, topic:str, packet:dict):
        """Publish packet"""
        self.__mqtt_client.publish(topic, payload=json.dumps(packet))



if __name__ == "__main__":
    offline = Offline()
    offline.main()

     