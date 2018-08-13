from flask import Flask,url_for,request
import requests
import json
import pymongo
import paho.mqtt.client as mqtt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dockerData"]

app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("fuck")
    client.subscribe("you")
    client.subscribe("abc")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    mycol = mydb[str(msg.topic)]
    data = str(msg.payload)
    userData = { "NAME" : str(msg.topic), "talk" : data[2:-1]}
    insertData = mycol.insert_one(userData)
    # print(msg.topic)
    # print(data[2:-1])

@app.route('/')
def index():
    data = []
    user1_col = mydb["fuck"]
    for x in user1_col.find({},{ "_id": 0, "NAME": 1, "talk": 1 }):
        data.append(x)

    print(json.dumps(data))
    # data = str(data)

    return json.dumps(data)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.0.108')
    client.loop_start()

    app.run(host='127.0.0.1')




