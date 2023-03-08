
import paho.mqtt.client as mqtt
import json, socket, threading
from handler import Handler
from constants import *


# class TYPE(enumerate):
#     TX = 0
#     TX_RX = 1


class Forwarder():


    def __init__(self, host : str, port : int):
        self.host   = host
        self.port   = port
        self.__lock = threading.Lock()
        self.__socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__handler = Handler(DEFAULT_GATEWAY_ID)
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="forwarder")


    def __setup__(self):
        self.__socket.bind(("0.0.0.0" , self.port))
        self.__mqtt_client.on_connect    = self.__mqtt_on_connect__
        self.__mqtt_client.on_message    = self.__mqtt_on_message__
        self.__mqtt_client.on_disconnect = self.__mqtt_on_disconnect__
        self.__mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.__mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


    def __loop__(self):
        while True:
            print("UDP Waiting for data...")
            data, address = self.__socket.recvfrom(4096)
            print('received {} bytes from {}'.format(len(data), address))
            print("received message:", data)
            self.__handle__(data)
        

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
                print("TX_ACK Sent")
            packet = data[4:].decode("utf-8")
            self.__publish__(packet)
        elif pkt_type == PKT_PULL_ACK:
            self.__handler.pull_ack(data)
        elif pkt_type == PKT_PUSH_ACK:
            self.__handler.push_ack(data)


    def __periodic_task__(self):
        try:
            data = self.__handler.pull_data()
            with self.__lock:
                self.__socket.sendto(data, (self.host, self.port))
                print("PULL_DATA Sent")
        except:
            pass
        finally:
            threading.Timer(PULL_DATA_FREQUENCY, self.__periodic_task__).start()

                        
    def __one_shot_task__(self, message:mqtt.MQTTMessage):
        try:
            topic = message.topic
            payload = eval(message.payload)
            print(payload)
            if topic == MQTT_TOPIC_FORWARDER_IN:
                data = json.dumps(payload)
                data = self.__handler.push_data(data)
                with self.__lock:
                    self.__socket.sendto(data, (self.host, self.port))
                    print("PUSH_DATA Sent")
            elif topic == MQTT_TOPIC_FORWARDER_NWK:
                self.__network_config__(payload)
                print("LoRa Server Set")
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
        client.subscribe(MQTT_TOPIC_FORWARDER_NWK)


    def __mqtt_on_disconnect__(self, client : mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")


    def __publish__(self,  packet:str):
        """Publish packet to Gateway System"""
        print("Publishing Packet", packet)
        self.__mqtt_client.publish(MQTT_TOPIC_FORWARDER_OUT, packet)

    def __network_config__(self,  payload:dict):
        host  = payload["gateway_conf"]["server_address"]
        port  = payload["gateway_conf"]["server_post"]
        gw_id = payload["gateway_conf"]["gateway_id"]
        with self.__lock:
            self.host = host
            self.port = port
            self.__handler.set_gateway_id(gw_id)

if __name__ == "__main__":
    forwarder = Forwarder("192.168.1.113", 1700)
    forwarder.main()