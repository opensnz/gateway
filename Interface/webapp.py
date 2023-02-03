from flask import Flask, render_template, request, Response, jsonify, abort
from modules.constants import *
import paho.mqtt.client as mqtt
import json

#########################################################################

mqtt_client = mqtt.Client(transport="tcp",client_id="transceiver")
mqtt_client.username_pw_set("transceiver","transceiver#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.publish(MQTT_TOPIC_TRANSCEIVER_OUT, payload=json.dumps({"packet":""}))

#########################################################################

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')



#########################################################


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=False)