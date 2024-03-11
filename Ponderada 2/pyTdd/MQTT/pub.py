import paho.mqtt.client as mqtt
import time
import json

# Carregar dados do arquivo JSON
sensors_file = open ('sensors.json')
json_array = json.load(sensors_file)

class DynamicMessage:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def message(self):
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return str(attributes)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_publisher")

client.connect("localhost", 1891, 60)

messages_list = []
for item in json_array:
    json_item = DynamicMessage(**item).message()
    messages_list.append(json_item)
try:
    while True:
        for message in messages_list:
            client.publish("sensors/topic", message)
            print(f"Publicado: {message}")
            time.sleep(2)
except KeyboardInterrupt:
    print("Publicação encerrada")

client.disconnect()
