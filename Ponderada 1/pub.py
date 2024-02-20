import paho.mqtt.client as mqtt
import time
import json

message_json = '{"teste1": "santos", "teste2": "futebol", "teste3": "clube"}'

message = json.loads(message_json)


class DynamicMessage:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return str(attributes)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_publiser")

client.connect("localhost", 1891, 60)

to_be_published = DynamicMessage(**message)

print(to_be_published)

try:
    while True:
        message = "Hello MQTT" + time.strftime("%H:%M:%S")
        client.publish("sensors/topic", to_be_published)
        print(f"Publicado: {to_be_published}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Publicação encerrada")

client.disconnect
