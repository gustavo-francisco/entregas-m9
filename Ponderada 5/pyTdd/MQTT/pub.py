import os
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt
import json
import time

load_dotenv() # Le variáveis de ambiente do arquivo .env

# Configurações do broker
broker_address = os.getenv("BROKER_ADDR")
port = 8883
topic = "my/test/topic"
username = os.getenv("HIVE_USER")
password = os.getenv("HIVE_PSWD")

# Carregar dados do arquivo JSON
sensors_file = open ('sensors.json')
json_array = json.load(sensors_file)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK received with code {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Mid: {mid}")

def on_message(client, userdata, msg):
    print(f"{msg.topic} (QoS: {msg.qos}) - {msg.payload.decode('utf-8')}")

class DynamicMessage:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def message(self):
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return str(attributes)

client = paho.Client(paho.CallbackAPIVersion.VERSION2, "Publisher",
                     protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)

client.on_message = on_message
client.on_publish = on_publish

client.connect(broker_address, port=port)

messages_list = []
for item in json_array:
    json_item = DynamicMessage(**item).message()
    messages_list.append(json_item)
try:
    while True:
        for message in messages_list:
            client.publish(topic, payload=message, qos=1)
            print(f"Publicado: {message}")
            time.sleep(2)
except KeyboardInterrupt:
    print("Publicação encerrada")

client.disconnect()
