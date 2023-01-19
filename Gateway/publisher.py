
import paho.mqtt.client as mqtt
import requests, json
from datetime import datetime
from constants import *

mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")

json_post = {
  "DevAddr": "012cdf67",
  "NwkSKey": "663c625cdd8f82095162525bd9b26926",
  "AppSKey": "0efd6c3eee67d32e05e8dc682795d9ca",
	"FCnt" : 8,
	"FPort": 2,
	#"payload":"68100001020304050681319012002C601300002C150515002C330303033556353700043600303016111119200012005716"
	"payload":"6810AAAAAAAAAAAAAA81319012002C601300002C150515002C33030303355635370004360030301611111920001200E816"
}
DevEUI = "b53fcaaa8725fe1b"
AppKey = "45abd993fa42864305fd20b63b21b80d"
AppEUI = "0000000000000000"
DevNonce="1111"
json_post["DevEUI"]=DevEUI
json_post["AppEUI"]=AppEUI
json_post["AppKey"]=AppKey
json_post["DevNonce"]=DevNonce
print(json.dumps(json_post, indent=4))

resp = requests.post("http://192.168.1.241:8080/ConfirmedDataUp", json=json_post)

print("response status code", resp.status_code)
message = {
  "rxpk": [
    {
      "time": datetime.utcnow().isoformat()+'Z',
      "tmms": int(datetime.now().timestamp()),
      "tmst": int(datetime.now().timestamp()),
      "freq": 868.1,
      "chan": 0,
      "rfch": 0,
      "stat": 1,
      "modu": 'LORA',
      "datr": 'SF7BW125',
      "codr": '4/5',
      "rssi": -97,
      "lsnr": 12,
      "size": 23,
      "data": 'AAAAAAAAAAAAG/4lh6rKP7UREeiSEHc='
    }
  ]
  #,"stat":{"time":"2023-01-14 12:50:05 UTC","lati":6.152011316947985,"long":1.2591783408612136,"alti":5,"rxnb":51,"rxok":51,"rxfw":7,"ackr":7,"dwnb":79,"txnb":7}
}

message["rxpk"][0]["data"] = resp.json()["PHYPayload"]


#print(resp.json())
mqtt_client.username_pw_set("transceiver","transceiver#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":DevEUI+json_post["payload"]}))
