import urllib.request
import time
import paho.mqtt.client as mqtt
import sqlite3
import os
from constants import *
from Gateway.database import Database

db = Database
database_name = "offline.db"
table_name = "offline_data"

conn = sqlite3.connect(database_name)
c = conn.cursor()
c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT, DevEUI VARCHAR(16) NOT NULL, Packet TEXT, time TEXT)")


def check_internet():
    try :
        urllib.request.urlopen('https://www.google.com')
        return True
    except :
        return False
    
def publish_message():
    client = mqtt.Client(transport="tcp",client_id="##################")
    client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.publish(MQTT_TOPIC_CONNECTION, "Connected to the internet!") 
    client.disconnect()

def insert_data(dev_eui, packet):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    c.execute(f"INSERT INTO {table_name} (DevEUI, Packet, time) VALUES (?, ?, ?)", (dev_eui, packet, current_time))
    conn.commit()

def send_data():
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    for row in rows:
        dev_eui = row[1]
        packet = row[2]
        current_time = row[3]
        db.__insert_data__(DevEUI=dev_eui)
        message = f"Packet from {dev_eui} received on {current_time}: {packet}"
        client = mqtt.Client(transport="tcp",client_id="##################")
        client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.publish(MQTT_TOPIC_RECONNECTION, message)
    c.execute(f"DELETE FROM {table_name}")
    conn.commit()
    os.remove(database_name)

while True:
    if check_internet():
        publish_message()
        send_data()
    else:
        insert_data(dev_eui, packet)
    time.sleep(2)

     