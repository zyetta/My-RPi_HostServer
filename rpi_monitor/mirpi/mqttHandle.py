from mirpi.models import  User, Devices, Preferences, Power, Hubs, Sensors
from mirpi import db
from datetime import datetime
import paho.mqtt.client as mqtt
from time import sleep, time
import json, ast
import mirpi.cnst as const
import subprocess, platform
from mirpi.preferences import CPUTempExceeded
  
# Title:     Store Sensor Data
# Desc:      Stores the sensor data that is recieved from the relevant handler function
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def storeSensor(hold):
    pref_hold = Preferences.query.get_or_404(1)
    try:
        sensor = Sensors(
            unix=int(time()),
            curr=float(hold["CURR"]),
            volt=float(hold["VOLT"]),
            temp=float(hold["TEMP"]),
            hub_id=int(hold["ID"]))
        print(sensor)
        device = Hubs.query.filter_by(id=int(hold["ID"])).first()
        if device:
            if float(hold["CURR"]) > float(pref_hold.curr_max):
                print("Exceeded")
                if pref_hold.curr_exceeded:
                    try:
                        try:
                            print("Exceeded")
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
        try:
            db.session.add(sensor)
            db.session.commit()
        except:
            db.session.rollback()
    except Exception as e:
        print(e)


# Title:     Store Device Information
# Desc:      Store the Devices Information that is recieved from the relevant handler function
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def storeDevInfo(hold):
    pref_hold = Preferences.query.get_or_404(1)
    device = Devices.query.filter_by(ip=str(hold["IP"])).first()
    try:
        if device:
            print(hold)
            device.cpu_usage = float(hold["CPU"])
            device.memory_usage = float(hold['MEM'])
            device.memory_total = float(hold['MEMTOT'])
            mac_hold = str(hold['MAC'])
            mac = mac_hold[2:4] + "-" + mac_hold[4:6] + "-" + mac_hold[6:8] + \
                "-" + mac_hold[8:10] + "-" + \
                mac_hold[10:12] + "-" + mac_hold[12:14]
            device.mac = str.upper(mac)
            device.cpu_temp = float(hold['TEMP'])
            device.last_accessed = datetime.utcnow()
            device.initiated = 1

            if(float(hold["CPU"]) > pref_hold.status_threash):
                device.status = "Active"
            else:
                device.status = "Idle"
            if float(hold['TEMP']) > pref_hold.temp_max:
                if Preferences.query.first().temp_exceeded:
                    try:
                        CPUTempExceeded(Preferences.query.first().email,
                                        device.ip, device.mac, device.hub, device.hub_location,
                                        device.username, device.last_accessed, device.hostname,
                                        float(hold['TEMP']), device.memory_usage, device.cpu_usage, device.memory_total)
                    except Exception as e:
                        print(e)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    except Exception as e:
        db.session.rollback()
        print(e)

# Title:     MQTT On Connect Handler
# Desc:      Handler function executed on client connect
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker 1")
        global Connected
        Connected = True
        client.subscribe("sensors/#", 0) 
        client.subscribe("devices/#", 0) 
        client.subscribe("hub/#", 0) 
        client.subscribe("hub/calib/+/complete", 0)
        try:
            hold =  Preferences.query.first()
            hold.broker_connected = 1
            hold.date_connected = datetime.utcnow() 
            db.session.commit()
        except:
            pass      
    else:
        print("Connection failed")

# Title:     MQTT On Disconnect Handler
# Desc:      Handler function executed on client disconnect
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def on_disconnect(client, userdata, rc):    
    print("Disconnected")
    Connected = False
    try:      
        hold =  Preferences.query.first()
        hold.broker_connected = 1
        hold.date_connected = datetime.utcnow() 
        db.session.commit()
        while(Connected == False):
            for i in const.broker_address:
                try:
                    client_1.connect(i, const.broker_port, const.broker_timeOut)
                    Connected = True
                    break
                except Exception as e:
                    print(e)
                    hold =  Preferences.query.first()
                    hold.broker_connected = 1
                    hold.date_connected = datetime.utcnow() 
                    db.session.commit()
                    sleep(2)     
    except:
        pass   

# Title:     MQTT On Message Handler
# Desc:      Will process payload, and perform appropriate actions
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def on_message(client,userdata, msg):   
    topic = str(msg.topic)
    msg = ast.literal_eval(str(msg.payload.decode("utf-8")))
    if(topic[0:7] == "sensors"): 
        storeSensor(msg)   
    elif(topic[0:3] == "hub"):
        print(msg)
    elif(topic[0:7] == "devices"):
        storeDevInfo(msg) 


# Title:     MQTT On Subscribe Handler
# Desc:      Prints message on successful subscribe
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed")
    pass

Connected = False
hold =  Preferences.query.first()
hold.broker_connected = 0
hold.date_connected = datetime.utcnow() 
db.session.commit()

while(Connected == False):
    try:      
        client_1 = mqtt.Client()
        client_1.on_message = on_message
        client_1.on_connect = on_connect
        client_1.on_subscribe = on_subscribe
        client_1.on_disconnect = on_disconnect
        client_1.username_pw_set(username = const.broker_username, password=const.broker_password)
        for i in const.broker_address:
            try:
                client_1.connect(i, const.broker_port, const.broker_timeOut)
                client_1.loop_start()
                Connected = True
                break
            except Exception as e:
                print("Error Connecting to: " + i)        
                sleep(5)   
    except Exception as e:
        print(e)



def hubInit(HUB):
    try:
        payload = "{'0':'" + str(HUB.ip) + "','1':'" + str(HUB.id) + "','2':'0','3':'0'}"
        payload = str(payload)
        client_1.publish("hub/init", payload)
    except Exception as e:
        print(e)
    

def hubControl(HUB, COMMAND, Device_Pin):
    try:
        payload = "{'0':'" + str(HUB.ip) + "','1':'" + str(HUB.id) + "','2':'" + str(Device_Pin) + "','3':'" + str(COMMAND) + "'}"
        payload = str(payload)
        print(payload)
        client_1.publish("hub/" + str(HUB.id), payload, qos=2, retain=True)
        sleep(1)
        payload = "{'0':'" + str(HUB.ip) + "','1':'" + str(HUB.id) + "','2':'" + str(0) + "','3':'" + str(COMMAND) + "'}"
        payload = str(payload)
        print(payload)
        client_1.publish("hub/" + str(HUB.id), payload, qos=2, retain=True)
        return 1
    except Exception as e:
        print(e)
        return 0
  