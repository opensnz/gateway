
import paho.mqtt.client as mqtt
import json, time
import threading
import serial
from constants import *
from dorji import *


class Transceiver():


    def __init__(self):
        self.__mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")
        self.__configuring = False

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
        # Transceiver radio configuration 
        conf = self.__load_config__()
        while not self.__config__(  conf["radio_conf"]["frequency"],
                                    conf["radio_conf"]["bandwidth"],
                                    conf["radio_conf"]["spreading_factor"]):
            time.sleep(1)

    def __loop__(self):
        while True:
            print("Transceiver Waiting for data...")
            # Read incoming data
            self.__ser.reset_input_buffer()
            data =  self.__ser.read()
            time.sleep(0.01)
            while  self.__ser.in_waiting:
                data = data +  self.__ser.read( self.__ser.in_waiting)
                if self.__ser.in_waiting == 0:
                    time.sleep(0.01)
            if not self.__configuring:
                payload = data[1:]
                if len(payload) > TRANSCEIVER_DATA_MIN_SIZE:
                    threading.Timer(0, self.__one_shot_task__, args=(payload,)).start()
            else:
                self.__configuring = False


    def __one_shot_task__(self, payload:bytes):
        try:
            self.__mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":payload.hex()}))
        except:
            pass


    def __config__(self, frequency : int, bandwith : int, spreading_factor : int) -> bool:
        cmd = dorji_cmd_config(frequency, bandwith, spreading_factor)
        if cmd == None:
            return False
        self.__ser.reset_output_buffer()
        self.__configuring = True
        self.__ser.write(cmd)
        return True
    
    def __load_config__(self) -> dict:
        while True:
            try :
                with open(CONFIG_FILE_PATH, "r") as file:
                    config = json.load(file)
                    return config
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

    def __mqtt_task__(self, message:mqtt.MQTTMessage):
        try:
            topic = message.topic
            if topic == MQTT_TOPIC_TRANSCEIVER_IN:
                data = json.loads((b''+message.payload).decode())
                self.__ser.write(bytes.fromhex(data["packet"]))
            elif topic == MQTT_TOPIC_TRANSCEIVER_CONF:
                conf = json.loads((b''+message.payload).decode())
                while not self.__config__(  conf["frequency"],
                                            conf["bandwidth"],
                                            conf["spreading_factor"]):
                    time.sleep(1)
        except Exception as e:
            print(e)
            pass
        finally:
            pass

    def __mqtt_on_message__(self,  client : mqtt.Client, userdata, message:mqtt.MQTTMessage):
        print("MQTT_Message received")
        threading.Timer(0, self.__mqtt_task__, args=(message,)).start()


    def __mqtt_on_connect__(self, client : mqtt.Client, userdata, flags, rc):
        print("MQTT_Client connected")
        client.subscribe(MQTT_TOPIC_TRANSCEIVER_IN)
        client.subscribe(MQTT_TOPIC_TRANSCEIVER_CONF)


    def __mqtt_on_disconnect__(self, client : mqtt.Client, userdata, rc):
        print("MQTT_Client disconnected")




if __name__ == "__main__":
    transceiver = Transceiver()
    transceiver.main()

