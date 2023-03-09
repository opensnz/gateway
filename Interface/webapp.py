import secrets
from flask import Flask, redirect, render_template, request, Response, jsonify, abort, url_for
from modules.constants import *
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from modules.database import Database
from modules.telemetry import *
from modules.constants import *





#########################################################################

mqtt_client = mqtt.Client(transport="tcp",client_id="interface")
mqtt_client.username_pw_set("interface","interface#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

#########################################################################

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/status")
def status():
    db = Database()
    db.open()
    db.close()
    network = NETWORK()
    cpu = CPU()
    disk = DISK()
    ram=RAM()
    platform=PLATFORM()
    return render_template( 'status.html', interfaces=network.interfaces, cpu=cpu, disk=disk, ram=ram, platform=platform )

@app.route("/addDevice")
def addDevice():
    return render_template('addDevice.html')



@app.route("/system",  methods=['GET', 'POST'])
def system():
    system = None
    with open(CONFIG_FILE_PATH, "r") as file:
        system = json.load(file)
        print(system)
    return render_template('network.html', system=system)


@app.route("/device/all",  methods=['GET', 'POST'])
def devices():
    db = Database()
    db.open()
    devices = db.get_devices()
    print(devices)
    db.close()
    return render_template("peripherique.html", devices=devices)
    
@app.route("/device/add" , methods=['GET' , 'POST'])
def add_device():
    body = request.json
    print(body)
    db = Database()
    db.open()
    status = db.insert_device(body["DevEUI"], body["AppEUI"], body["AppKey"])
    db.close()
    client = mqtt.Client(transport="tcp",client_id="interface")
    mqtt_client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.publish(MQTT_TOPIC_GATEWAY_DEV, payload=json.dumps(body))
    client.disconnect()
    if status:
        return redirect("/peripherique.html")
    else:
        return jsonify({"message": "Device addition failed."}), 500

   

@app.route("/device/delete", methods=["POST"])
def delete_devices():
    body = request.json
    db = Database()
    db.open()
    for DevEUI in body["DevEUIs"]:
        state = db.delete_device(DevEUI)
        if not state:
            db.close()
            return Response(status=500)
    db.close()
    return Response(status=200)  

 


@app.route('/network', methods=['POST'])
def save_json():
    data = request.get_json()
    client = mqtt.Client(transport="tcp",client_id="interface")
    mqtt_client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.publish(MQTT_TOPIC_GATEWAY_DEV, json.dumps(data)) 
    client.disconnect()
    with open(CONFIG_FILE_PATH, "w") as file:
        json.dump(data, file)
    return jsonify({"success": True})



#########################################################


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=88, debug=False)



   