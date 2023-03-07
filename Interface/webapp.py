import secrets
from flask import Flask, redirect, render_template, request, Response, jsonify, abort, url_for
from modules.constants import *
import paho.mqtt.client as mqtt
import json
from modules.database import Database
from modules.telemetry import *



#########################################################################

mqtt_client = mqtt.Client(transport="tcp",client_id="interface")
mqtt_client.username_pw_set("interface","interface#2022")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

#########################################################################

app = Flask(__name__)

@app.route("/")
def index():
    db = Database()
    db.open()
    db.close()
    network = NETWORK()
    cpu = CPU()
    disk = DISK()
    ram=RAM()
    platform=PLATFORM()
    return render_template('index.html', interfaces=network.interfaces, cpu=cpu, disk=disk, ram=ram, platform=platform )

@app.route("/addDevice" , methods=['GET' , 'POST'])
def addDevice():
    return render_template('addDevice.html')

#@app.route('/peripherique' , methods=['GET', 'POST'])
#def peripherique():
#    db = Database()
#    db.open()
#    devices = db.get_devices()
#    print(devices)
#    db.close()
#    return render_template('peripherique.html',  devices=devices)


@app.route("/system",  methods=['GET', 'POST'])
def system():
    system = Telemetry()
    return render_template('network.html', system=system)

#@app.route('/peripherique' , methods=['GET', 'POST'])
#def peripherique():
#    db = Database()
#    db.open()
#    devices = db.get_devices()
#    print(devices)
#    db.close()
#    return render_template('peripherique.html',  devices=devices)


#@app.route("/system",  methods=['GET', 'POST'])
#def system():
#    db = Database()
#    db.open()
#    db.close()
#    network = NETWORK()
#    return render_template('network.html')


@app.route("/device/all",  methods=['GET', 'POST'])
def devices():
    db = Database()
    db.open()
    devices = db.get_devices()
    print(devices)
    db.close()
    #return jsonify(devices)
    return render_template("peripherique.html", devices=devices)



@app.route("/device/add" , methods=['GET' , 'POST'])
def add_device():
    body = request.json
    print(body)
    db = Database()
    db.open()
    state = db.insert_device(body["DevEUI"], body["AppEUI"], body["AppKey"])
    db.close()
    #return render_template("peripherique.html")
    if state:
        return Response(status=200)
    else:
        return Response(status=500)  
    
   

@app.route("/device/delete" , methods=['GET' , 'POST'])
def delete_device():
    body = request.json
    db = Database()
    db.open()
    state = db.delete_device(body["DevEUI"])
    db.close()
    if state:
        return Response(status=200)
    else:
        return Response(status=500)   

@app.route("/network",  methods=['GET', 'POST'])
def notwork():
    system = Telemetry().to_json()
    return jsonify(json.loads(system))


#########################################################


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=88, debug=False)



   