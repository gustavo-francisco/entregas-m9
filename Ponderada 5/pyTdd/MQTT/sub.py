import os
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt
import sqlite3

load_dotenv() # Le variáveis de ambiente do arquivo .env

# Configurações do broker
broker_address = os.getenv("BROKER_ADDR")
port = 8883
topic = "my/test/topic"
username = os.getenv("HIVE_USER")
password = os.getenv("HIVE_PSWD")

conn = sqlite3.connect('C:/Users/Inteli/Documents/GitHub/entregas-m9/Ponderada 5/metabase-data/dados.db')
cursor = conn.cursor()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"CONNACK received with code {reason_code}")
    client.subscribe(topic, qos=1)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(f"{msg.topic} (QoS: {msg.qos}) - {msg.payload.decode('utf-8')}")
    cursor.execute("INSERT INTO dados (valor) VALUES (?)", (msg.payload.decode(),))
    conn.commit()


# Instanciação do cliente
client = paho.Client(paho.CallbackAPIVersion.VERSION2, "Subscriber",
                     protocol=paho.MQTTv5)
client.on_connect = on_connect

# Configurações de TLS
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)  # Configuração da autenticação

client.on_message = on_message

# Conexão ao broker
client.connect(broker_address, port=port)

# Loop de espera por mensagens
client.loop_forever()