
import socket, requests
import json, threading
from constants import *
from handler import Handler

class Forwarder():

    def __init__(self, server : str, port : int):
        self.server = server
        self.port   = port
        self.__socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__handler = Handler(gatewayID='5b4931f97b1c0a8e')
        self.__running = False
        


    
    def __start__(self):
        self.__running = True
        self.__socket.bind(("0.0.0.0" , self.port))
        self.__periodic_task__()
        while True:
            print("Waiting for data...")
            data, address = self.__socket.recvfrom(4096)
            print('received {} bytes from {}'.format(len(data), address))
            print("received message:", data)
            self.__handle__(data)
        

    def run(self) -> None:
        """run packet forwarder forever"""
        try :
            print("Packet Forwarder running...")
            self.__start__()
        except Exception as e:
            print("Exception", e)
            self.__running = False
            pass
    

    def __handle__(self, data):
        # Receiving message from the LoRa Server
        pkt_type = data[3]
        if pkt_type == PKT_PULL_RESP:
            print("PKT_PULL_RESP")
            self.__handler.pull_resp(data)
            print("PKT_TX_ACK")
            data = self.__handler.tx_ack()
            self.__socket.sendto(data, (self.server, self.port))
        elif pkt_type == PKT_PULL_ACK:
            print("PKT_PULL_ACK")

    def __periodic_task__(self):
        threading.Timer(PULL_DATA_FREQUENCY, self.__periodic_task__).start()
        data = self.__handler.pull_data()
        print("PKT_PULL_DATA")
        self.__socket.sendto(data, (self.server, self.port))
        import time
        time.sleep(5)
        #QDdtywEgCgACq83v7u7u7g==
        #QDdtywEADwAC+s9gNxcTrg==
        data = '{"rxpk":[{"time":"2023-01-11T14:42:11Z","tmms":1357483331,"tmst":1673448131,"chan":0,"rfch":0,"stat":1,"freq":868.1,"brd":0,"rssi":-60,"datr":"SF7BW125","modu":"LORA","codr":"4/5","lsnr":7,"size":23,\
        "data":"QDdtywEADwAC+s9gNxcTrg=="}]\
        ,"stat":{"time":"2023-01-11 12:50:05 UTC","lati":6.152011316947985,"long":1.2591783408612136,"alti":5,"rxnb":51,"rxok":51,"rxfw":7,"ackr":7,"dwnb":79,"txnb":7}\
        }'
        data = self.__handler.push_data(data)
        self.__socket.sendto(data, (self.server, self.port))
        print("PKT_PUSH_DATA")
        
        # AppEUI = '0000000000000000'
        # DevEUI = '606018dc86d7e592'
        # AppKey = 'ebd350cb50aa25d34e16019469ca3e75'
        # DevNonce= "FF15"
        # post_json={"AppEUI":AppEUI, "DevEUI":DevEUI, "AppKey":AppKey, "DevNonce":DevNonce}
        # data = json.loads(data)
        # resp = requests.post("http://localhost:8080/JoinRequest", json=post_json)
        # data["rxpk"][0]['data'] = resp.json()["PHYPayload"]
        # print("PKT_PUSH_DATA", data)
        # data = json.dumps(data)
        # data = self.__handler.push_data(data)
        # self.__socket.sendto(data, (self.server, self.port))
        if self.__running == False:
            self.__socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.__start__()
                        



forwarder = Forwarder("192.168.1.13", 1700)

forwarder.run()