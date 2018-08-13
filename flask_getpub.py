from flask import Flask,url_for,request
from flask_mqtt import Mqtt
from flask import render_template
import requests
import json
import pymongo
import paho.mqtt.client as mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '192.168.0.116'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  
mqttr = Mqtt(app)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["flask"]

@app.route('/')
def index():
    return 'Index Hello World'

@mqttr.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqttr.subscribe('user1')
    mqttr.subscribe('user2')
    mqttr.subscribe('user3')

@mqttr.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    p = json.loads(payload)
    flask_col = mydb[str(message.topic)]
    insertData = flask_col.insert_one(p)  
    print("-------msg-------")
    # print('name  :', p['name'])
    # print('email :', p['email'])
    print(payload)

@app.route('/api/v1.0/mqtt/pub/<want_to_pub>', methods=['GET'])
def pub_my_msg(want_to_pub):
    if len(want_to_pub) == 0:
        abort(404)
    data = []
    flask_col = mydb[str(want_to_pub)]
    for x in flask_col.find({},{ "_id": 0 }):
        data.append(x)
    mqttr.publish('my',want_to_pub )
    return json.dumps(data)
if __name__ == '__main__':
    # client = mqtt.Client()
    # client.connect("192.168.0.116")
    app.run(host = "127.0.0.1" , debug=True)