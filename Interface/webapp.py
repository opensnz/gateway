from flask import Flask, render_template, request, Response, jsonify, abort
from modules.constants import *
import paho.mqtt.client as mqtt
import json
from modules.telemetry import Telemetry

#########################################################################

mqtt_client = mqtt.Client(transport="tcp",client_id="interface")
mqtt_client.username_pw_set("interface","interface#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

#########################################################################

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')


@app.route("/system")
def system():
   system = Telemetry().to_json()
   return jsonify(json.loads(system))



#########################################################


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=88, debug=False)



   