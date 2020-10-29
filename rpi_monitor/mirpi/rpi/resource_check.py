import paho.mqtt.client as mqtt
from time import sleep
import json, os, socket, psutil
from uuid import getnode as get_mac
import random

broker_address=["10.42.0.2", "mosquitto", "10.42.0.2", "10.42.0.1"]
broker_port = 1883
refresh_rate = 1
time_out = 45
username = "mqtt"
password = "gJGResE%0puwsX8%V$tp*01z2RJz0u88OFdjkDyO7*V0Yjo"
sleep(5)
cpu_usage =  psutil.cpu_percent()
sm = psutil.virtual_memory()

Closing = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global Connected    
        try: 
                global cpu_usage
                global sm
                mem_tot = sm.total
                mem_used = sm.used
                temp = random.randint(65, 66)
                mac = hex(get_mac())
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                        s.connect(('10.255.255.255', 1))
                        ip = s.getsockname()[0]

                        mqtt_topic = "devices/" + str(ip)
                        
                except:
                        ip = None
                        mqtt_topic = "devices/Error"
                finally:
                        mqtt_payload = str({"CPU": cpu_usage,
                        "MEM": mem_used, "MEMTOT": mem_tot,
                        "TEMP": temp, "MAC": mac, "IP": ip})
                        client.publish(mqtt_topic, mqtt_payload)
        except Exception as e:
                print(e)
        finally:
                Connected = True


def on_message(client,userdata, msg):           
        pass  
    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed")
    pass

def on_publish(client,userdata,result):
    global Closing
    Closing = 1


Connected = False
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.username_pw_set(username = username, password=password)
for i in range(10):
        address = broker_address[i % 3]
        try:
                client.connect(address, broker_port, time_out)
                print(address)
                client.loop_start()
                break
        except Exception as e:
                print(e)
                print(str(address) + " Not Found. Trying Retrying")

while(1):
        if Closing == 1:
                break
