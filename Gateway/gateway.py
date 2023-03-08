import paho.mqtt.client as mqtt
import json
import time, threading
from datetime import datetime
from database import Database
from encoder import Encoder
from constants import *


# class TYPE(enumerate):
#     TX = 0
#     TX_RX = 1


class STATUS(enumerate):
    JOIN_REQUEST = 0
    CONFIRMED_DATA_UP = 1

class Gateway():


    def __init__(self):
        self.__mapping__ = dict()
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="gateway")


    def __setup__(self):
        _db = Database()
        _db.open()
        _db.create_tables()
        _db.close()
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        """Main loop sleep 1 hour"""
        while True:
            time.sleep(3600)

  
    def main(self) -> None:
        """run gateway system forever"""
        try :
            print("Gateway System setting...")
            self.__setup__()
            print("Gateway System running...")
            """2 Threads run forever and concurrently"""
            self.__mqtt_client.loop_start()
            self.__loop__()
            
        except Exception as e:
            print("Exception in the main Thread:", e)
            self.__mqtt_client.loop_stop()
            raise Exception("Raised exception to relaunch Gateway Service")


    def __one_shot_task__(self, message:mqtt.MQTTMessage):
        # Save current date and time
        date_time = {
            "time": datetime.utcnow().isoformat()+'Z',
            "tmst": round(datetime.utcnow().timestamp()),
        }
        topic = message.topic
        topic_payload = eval(message.payload)
        if topic == MQTT_TOPIC_TRANSCEIVER_OUT:
            # Get DevEUI 
            DevEUI = topic_payload["packet"][:2*DEVICE_IDENTIFIER_SIZE]
            # Handle MQTT topic
            packet  = self.__topic_transceiver_handler__(topic_payload, date_time)
            if packet != None :
                # Publish packet
                self.__publish__(DevEUI, packet)
        elif topic == MQTT_TOPIC_FORWARDER_OUT:
            # Get DevEUI
            DevEUI = topic_payload["DevEUI"]
            if DevEUI in self.__mapping__.keys():
                # Handle MQTT topic
                packet = self.__topic_forwarder_handler__(topic_payload, date_time)
                if packet != None :
                    # Publish packet
                    self.__publish__(DevEUI, packet)
            else:
                pass
            



    def __join_request_packet__(self, device:dict) -> dict:
        packet = self.__generic_packet__()
        encoded = Encoder.join_request(device)
        # Filling packet
        packet["rxpk"][0]["size"] = encoded["size"]
        packet["rxpk"][0]["data"] = encoded["PHYPayload"]
        return packet


    def __unconfirmed_data_up_packet__(self, device:dict, payload:str) -> dict:
        packet = self.__generic_packet__()
        encoded = Encoder.unconfirmed_data_up(device, payload)
        # Filling packet
        packet["rxpk"][0]["size"] = encoded["size"]
        packet["rxpk"][0]["data"] = encoded["PHYPayload"]
        return packet
    

    def __generic_packet__(self) -> dict:
        packet = {
            "rxpk": [
                {
                    "time":'',
                    "tmms":0,
                    "tmst":0,
                    "chan":1,
                    "rfch":0,
                    "freq":868.3,
                    "stat":1,
                    "modu":"LORA",
                    "datr":"SF7BW125",
                    "codr":"4/5",
                    "rssi":-35,
                    "lsnr":5.0,
                    "size": 23,
                    "data": ''
                }
            ]
        }
        return packet
    
    def __update_packet__(self, packet:dict, topic_payload:dict, date_time:dict) -> dict:
        """Update packet with transceiver metadata, date and time"""
        packet["rxpk"][0]["time"] = date_time["time"]
        packet["rxpk"][0]["tmms"] = int(date_time["tmst"] - GPS_START_TIMESTAMP) * 1000
        packet["rxpk"][0]["tmst"] = date_time["tmst"]
        # Filling packet with transceiver metadata
        # packet["rxpk"][0]["freq"] = topic_payload["freq"]
        # packet["rxpk"][0]["datr"] = topic_payload["datr"]
        # packet["rxpk"][0]["rssi"] = topic_payload["rssi"]
        # packet["rxpk"][0]["lsnr"] = topic_payload["lsnr"]
        return packet


    def __mqtt_on_message__(self,  client:mqtt.Client, userdata, message:mqtt.MQTTMessage):
        print("MQTT_Message received")
        threading.Timer(0, self.__one_shot_task__, args=(message,)).start()


    def __mqtt_on_connect__(self, client:mqtt.Client, userdata, flags, rc):
        print("MQTT_Client connected")
        client.subscribe(MQTT_TOPIC_TRANSCEIVER_OUT)
        client.subscribe(MQTT_TOPIC_FORWARDER_OUT)


    def __mqtt_on_disconnect__(self, client:mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")
    
    ################### MQTT Subscribed Topics Handler ######################

    def __topic_transceiver_handler__(self, topic_payload:dict, date_time:dict):
        # Get DevEUI and device payload
        DevEUI = topic_payload["packet"][:2*DEVICE_IDENTIFIER_SIZE]
        payload= topic_payload["packet"][2*DEVICE_IDENTIFIER_SIZE:]
        # Get current device informations from database 
        _db = Database()
        _db.open()
        device = _db.get_device(DevEUI=DevEUI)
        _db.close()
        if device != None:

            # Check if device have already joined the server otherwise Join
            if device["NwkSKey"] is None or device["FCnt"] > 65530:
                # Save device's DevEUI for Join Accept
                self.__mapping__[DevEUI] = STATUS.JOIN_REQUEST
                # Save device's packet(with its raw payload) for later Unconfirmed or Conformed Data Up (Unconfirmed by default)
                packet = self.__generic_packet__()
                packet["rxpk"][0]["data"] = payload
                # Update packet with transceiver metadata, date and time 
                self.__update_packet__(packet, topic_payload, date_time)
                _db.open()
                _db.update_data(DevEUI=DevEUI, Packet=json.dumps(packet))
                _db.close()
                # LoRaWAN Join Request is needed
                # Encode packet by using RESP API service
                packet = self.__join_request_packet__(device)
                # Update packet with transceiver metadata, date and time 
                self.__update_packet__(packet, topic_payload, date_time)
                return packet

            else:
                # LoRaWAN Unconfirmed or Conformed Data Up is needed (Unconfirmed by default)
                # Encode packet by using RESP API service
                packet = self.__unconfirmed_data_up_packet__(device, payload)
                # Update packet with transceiver metadata, date and time 
                self.__update_packet__(packet, topic_payload, date_time)
                return packet
            
        return None
    
    def __topic_forwarder_handler__(self, topic_payload:dict, date_time:dict):
        DevEUI = topic_payload["DevEUI"]
        _db = Database()
        if self.__mapping__[DevEUI] == STATUS.JOIN_REQUEST:
            # Remove DevEUI from mapping dict
            self.__mapping__.pop(DevEUI)
            PHYPayload = json.loads(topic_payload["packet"])["txpk"]["data"]
            # Get device informations from database
            _db.open()
            device = _db.get_device(DevEUI=DevEUI)
            # Get saved packet
            packet = _db.get_data(DevEUI=DevEUI)["Packet"]
            _db.close()
            # Convert to python object
            packet = json.loads(packet)
            # LoRaWAN Join Accept is needed
            # Decode packet by using RESP API service
            # device is modified in the function(device is mutable object, so no need to get return dict)
            Encoder.join_accept(device, PHYPayload) 
            # Use saved packet's raw payload to encode uplink data
            # LoRaWAN Unconfirmed or Conformed Data Up is needed (Unconfirmed by default)
            # Encode packet by using RESP API service
            encoded_pk = self.__unconfirmed_data_up_packet__(device, packet["rxpk"][0]["data"])
            # Update saved packet
            packet["rxpk"][0]["size"] = encoded_pk["rxpk"][0]["size"]
            packet["rxpk"][0]["data"] = encoded_pk["rxpk"][0]["data"]
            return packet
        elif self.__mapping__[DevEUI] == STATUS.CONFIRMED_DATA_UP:
            return None


    ################### MQTT Publish  ######################

    def __publish__(self, DevEUI:str, packet:dict):
        """Publish packet with DevEUI to Packet Forwarder"""
        payload = {
            "DevEUI":DevEUI,
            "packet":json.dumps(packet)
        }
        print("Publishing Packet", payload["packet"])
        self.__mqtt_client.publish(MQTT_TOPIC_FORWARDER_IN, payload=json.dumps(payload))


    def __publish_config__(self, topic:str, config:dict):
        """Publish config data"""
        self.__mqtt_client.publish(topic, payload=json.dumps(config))
    

if __name__ == "__main__":
    gateway = Gateway()
    gateway.main()