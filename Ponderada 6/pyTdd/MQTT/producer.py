from confluent_kafka import Producer, Consumer, KafkaError
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

client = MongoClient('mongodb://localhost:27017/')
client.server_info()
db = client['provaM9']
collection = db['provitas']

load_dotenv()

broker_address = os.getenv("BROKER_ADDR")
print(broker_address)
port = 8883
topic = "sensorPonderada"
username = os.getenv("HIVE_USER")
password = os.getenv("HIVE_PSWD")

def read_config():
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                config[parameter] = value.strip()
    return config

def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

class DynamicMessage:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def message(self):
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return str(attributes)

file = open('data.json')
message = json.load(file)

messages_list = []

for item in message:
    json_item = DynamicMessage(**item).message()
    messages_list.append(json_item)

def produce(topic, config):
    producer = Producer(config)
    for message in messages_list:
        producer.produce(topic, message.encode('utf-8'), callback=delivery_callback)
        producer.flush()

def consume(topic, config):
    config["group.id"] = "python-group-1"
    config["auto.offset.reset"] = "earliest"

    consumer = Consumer(config)
    consumer.subscribe([topic])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                if msg.key() is not None:
                    key = msg.key().decode("utf-8")
                else:
                    key = None
                value = msg.value().decode("utf-8")
                print(f"Consumed message from topic {topic}: key = {key} value = {value}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def main():
    config = read_config()
    topic = "sensorPonderada"

    produce(topic, config)
    consume(topic, config)

main()
