import paho.mqtt.client as mqtt
import json
import time, threading, queue
from datetime import datetime
from database import Database
from encoder import Encoder
from constants import *
import urllib.request


class Gateway():


    def __init__(self):
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="gateway")
        self._db = Database()
        self.__queue = queue.Queue()
        self.__semaphore = threading.Semaphore()
        self.__status = True 


    def __setup__(self):
        self._db.open()
        self._db.create_tables()
        self._db.close()
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        """Main loop : performs JoinRequest every day"""
        while True:
            self._db.open()
            devices = self._db.get_devices()
            with self.__semaphore :
                for device in devices :
                    date_time = {
                        "time": datetime.utcnow().isoformat()+'Z',
                        "tmst": round(datetime.utcnow().timestamp()),
                    }
                    packet = self.__join_request_packet__(device)
                    # Update packet date and time 
                    self.__update_packet__(packet, None, date_time)
                    if packet != None :
                        # Publish packet
                        self.__publish__(packet)
                        time.sleep(1)

            time.sleep(JOIN_REQUEST_FREQUENCY)
  
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
        

    def __load_config__(self) -> dict:
        while True:
            try :
                with open(CONFIG_FILE_PATH, "r") as file:
                    config = json.load(file)
                    return config
            except:
                pass

    def __save_config__(self, config : dict) -> bool:
        while True:
            try :
                with open(CONFIG_FILE_PATH, "w") as file:
                    file.write(json.dumps(config, indent=4))
                    return True
            except:
                pass

    def check_internet(self):
        try :
            urllib.request.urlopen('https://www.google.com')
            return True
        except :
            return False

    def __one_shot_task__(self, message:mqtt.MQTTMessage):
        # Save current date and time
        date_time = {
            "time": datetime.utcnow().isoformat()+'Z',
            "tmst": round(datetime.utcnow().timestamp()),
        }
        topic = message.topic
        topic_payload = json.loads((b''+message.payload).decode())
        if topic == MQTT_TOPIC_TRANSCEIVER_OUT:
            # Get DevEUI 
            DevEUI = topic_payload["packet"][:2*DEVICE_IDENTIFIER_SIZE]
            # Handle MQTT topic
            packet  = self.__topic_transceiver_handler__(topic_payload, date_time)
            if packet == None :
                return 
            
            if self.__status :
                # Publish packet
                self.__publish__(packet)
            else :
                offline_packet = {}
                offline_packet["DevEUI"] = DevEUI
                offline_packet["Packet"] = packet["rxpk"][0]
                self.__publish_offline__(offline_packet)
        elif topic == MQTT_TOPIC_FORWARDER_OUT:
            # Handle MQTT topic
            packet = self.__topic_forwarder_handler__(topic_payload, date_time)
            if packet != None :
                # Publish packet
                self.__publish__(packet)
        elif topic == MQTT_TOPIC_GATEWAY_DEV:
            # Handle MQTT topic
            packet = self.__topic_device_handler__(topic_payload, date_time)
            if packet != None :
                # Publish packet
                self.__publish__(packet)
        elif topic == MQTT_TOPIC_GATEWAY_NWK:
            # Handle MQTT topic
            self.__topic_network_handler__(topic_payload)
        elif topic == MQTT_TOPIC_GATEWAY_STATUS:
            print(topic_payload)
            self.__status = topic_payload["status"]
            



    def __join_request_packet__(self, device:dict) -> dict:
        # Put DevEUI to queue before JoinRequest
        self.__queue.put(device["DevEUI"])
        encoded = Encoder.join_request(device)
        packet = self.__generic_packet__()
        # Filling packet
        packet["rxpk"][0]["size"] = encoded["size"]
        packet["rxpk"][0]["data"] = encoded["PHYPayload"]
        return packet


    def __unconfirmed_data_up_packet__(self, device:dict, payload:str) -> dict:
        # Acquire will block when gateway perfoms JoinRequest
        self.__semaphore.acquire()
        self.__semaphore.release()
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
        client.subscribe(MQTT_TOPIC_GATEWAY_DEV)
        client.subscribe(MQTT_TOPIC_GATEWAY_NWK)
        client.subscribe(MQTT_TOPIC_GATEWAY_STATUS)


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
        if device != None and device["NwkSKey"] != None:
            # LoRaWAN Unconfirmed or Conformed Data Up is needed (Unconfirmed by default)
            # Encode packet by using RESP API service
            packet = self.__unconfirmed_data_up_packet__(device, payload)
            # Update packet with transceiver metadata, date and time 
            self.__update_packet__(packet, topic_payload, date_time)
            return packet
        return None
    
    def __topic_forwarder_handler__(self, topic_payload:dict, date_time:dict=None):
        DevEUI = "" 
        PHYPayload = topic_payload["txpk"]["data"]
        packet_type = Encoder.packet_type(PHYPayload)
        if packet_type == "JoinAccept" : 
            DevEUI = self.__queue.get()
            # Get device informations from database
            _db = Database()
            _db.open() 
            device = _db.get_device(DevEUI=DevEUI)
            _db.close()
            Encoder.join_accept(device, PHYPayload)
            return None
        elif packet_type == "UnconfirmedDataDown" or packet_type == "ConfirmedDataDown": 
            return None

    def __topic_device_handler__(self, topic_payload:dict, date_time:dict=None):
        _db = Database()
        _db.open()
        device = _db.get_device(topic_payload["DevEUI"])
        _db.close()
        if device == None:
            return None
        packet = self.__join_request_packet__(device)
        # Update packet with transceiver metadata, date and time 
        self.__update_packet__(packet, topic_payload, date_time)
        return packet
    
    def __topic_network_handler__(self, topic_payload:dict):
        conf = self.__load_config__()
        radio_flag = False
        gateway_flag = False
        if "radio_conf" in topic_payload :
            radio_topic : dict = topic_payload["radio_conf"]
            radio_conf : dict = conf["radio_conf"]
            for key in radio_conf:
                if radio_conf.get(key) != radio_topic.get(key):
                    radio_flag = True
                    break
        if "gateway_conf" in topic_payload :
            gateway_topic : dict = topic_payload["gateway_conf"]
            gateway_conf : dict = conf["gateway_conf"]
            for key in gateway_conf:
                if gateway_conf.get(key) != gateway_topic.get(key):
                    gateway_flag = True
                    break
        if radio_flag or gateway_flag:
            # save config file
            self.__save_config__(topic_payload)
            if radio_flag:
                # notify transceiver
                self.__mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_CONF, 
                                           payload=json.dumps(topic_payload["radio_conf"]))
            if gateway_flag:
                # notify forwarder
                self.__mqtt_client.publish(MQTT_TOPIC_FORWARDER_CONF, 
                                           payload=json.dumps(topic_payload["gateway_conf"]))


    ################### MQTT Publish  ######################

    def __publish__(self, packet:dict):
        """Publish packet to Packet Forwarder"""
        self.__mqtt_client.publish(MQTT_TOPIC_FORWARDER_IN, payload=json.dumps(packet))

    def __publish_offline__(self, packet:dict):
        """Publish packet to Offline Service"""
        self.__mqtt_client.publish(MQTT_TOPIC_GATEWAY_OFFLINE, payload=json.dumps(packet))


    def __publish_config__(self, topic:str, config:dict):
        """Publish config data"""
        self.__mqtt_client.publish(topic, payload=json.dumps(config))
    

if __name__ == "__main__":
    gateway = Gateway()
    gateway.main()