
import paho.mqtt.client as mqtt
import json, sys, socket, threading
from datetime import datetime
from handler import Handler
from constants import *



class Forwarder():


    def __init__(self):
        self.host   = "localhost"
        self.port   = 1700
        self.__lock = threading.Lock()
        self.__socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__handler = Handler()
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="forwarder")



    def __setup__(self):
        conf = self.__load_config__()
        self.__config__(conf)
        self.__socket.bind(("0.0.0.0" , self.port))
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        while True:
            data, address = self.__socket.recvfrom(4096)
            self.__handle__(data)
    
    def __load_config__(self) -> dict:
        while True:
            try :
                with open(CONFIG_FILE_PATH, "r") as file:
                    conf = json.load(file)
                    return conf["gateway_conf"]
            except:
                pass
    
    def __config__(self, conf : dict):
        self.host = conf["server_address"]
        self.port = conf["server_port"]
        self.__handler.set_gateway_id(conf["gateway_id"])
        self.__handler.gateway_lon = conf["gateway_lon"]
        self.__handler.gateway_lat = conf["gateway_lat"]
        self.__handler.gateway_alt = conf["gateway_alt"]
        self.__handler.stat_interval  = conf["stat_interval"]
        self.__handler.alive_interval = conf["alive_interval"]

    def main(self) -> None:
        """run packet forwarder forever"""
        try :
            print("Packet Forwarder setting...")
            self.__setup__()
            print("Packet Forwarder running...")
            """3 Threads run forever and concurrently"""
            self.__periodic_task__()
            self.__mqtt_client.loop_start()
            self.__loop__()
            
        except Exception as e:
            print("Exception in the main Thread:", e)
            self.__mqtt_client.loop_stop()
            raise Exception("Raised exception to relaunch Packet Forwarder Service")
    

    def __handle__(self, data : bytes):
        # Receiving message from the LoRa Server
        pkt_type = data[3]
        if pkt_type == PKT_PULL_RESP:
            token_z = self.__handler.pull_resp(data)
            tx_data = self.__handler.tx_ack(token_z)
            with self.__lock:
                self.__socket.sendto(tx_data, (self.host, self.port))
            packet = data[4:].decode("utf-8")
            self.__publish__(packet)
        elif pkt_type == PKT_PULL_ACK:
            self.__handler.pull_ack(data)
        elif pkt_type == PKT_PUSH_ACK:
            self.__handler.push_ack(data)


    def __periodic_task__(self):
        try:
            timestamp = round(datetime.utcnow().timestamp())
            if (timestamp - self.__handler.stat_timestamp) >= self.__handler.stat_interval:
                self.__handler.stat_timestamp = timestamp
                data = self.__handler.push_stat()
                with self.__lock:
                    self.__socket.sendto(data, (self.host, self.port))
            if self.__handler.pkt__txnb == sys.maxsize - 1:
                self.__handler.lora_rxnb = 0
                self.__handler.lora_txnb = 0
                self.__handler.pkt__rxnb = 0
                self.__handler.pkt__txnb = 0
                self.__handler.pkt_acknb = 0
            data = self.__handler.pull_data()
            with self.__lock:
                self.__socket.sendto(data, (self.host, self.port))
        except:
            pass
        finally:
            threading.Timer(self.__handler.alive_interval, self.__periodic_task__).start()

                        
    def __one_shot_task__(self, message:mqtt.MQTTMessage):
        try:
            topic = message.topic
            payload = eval(message.payload)
            if topic == MQTT_TOPIC_FORWARDER_IN:
                data = json.dumps(payload)
                data = self.__handler.push_data(data)
                with self.__lock:
                    self.__socket.sendto(data, (self.host, self.port))
            elif topic == MQTT_TOPIC_FORWARDER_CONF:
                self.__config__(payload)
        except Exception as e:
            print(e)
            pass
        finally:
            pass


    def __mqtt_on_message__(self,  client : mqtt.Client, userdata, message:mqtt.MQTTMessage):
        print("MQTT_Message received")
        threading.Timer(0, self.__one_shot_task__, args=(message,)).start()


    def __mqtt_on_connect__(self, client : mqtt.Client, userdata, flags, rc):
        print("MQTT_Client connected")
        client.subscribe(MQTT_TOPIC_FORWARDER_IN)
        client.subscribe(MQTT_TOPIC_FORWARDER_CONF)


    def __mqtt_on_disconnect__(self, client : mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")


    def __publish__(self,  packet:str):
        """Publish packet to Gateway System"""
        self.__mqtt_client.publish(MQTT_TOPIC_FORWARDER_OUT, packet)


if __name__ == "__main__":
    forwarder = Forwarder()
    forwarder.main()