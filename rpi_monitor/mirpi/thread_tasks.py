from mirpi.user_functions import total_power, NetScan, ping_devices
from mirpi.globalVariables import network_scanning_timer, device_ping
from threading import Thread
from mirpi.models import Devices
from time import sleep

# Title:     Device State
# Desc:      Threaded Loop to capture Device State
# Author:    JJ MAREE
# Last Mod:  01-07-2020

# Title:     Total Power Consumption
# Desc:      Threaded Loop to capture Total Power Consumption
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def dev_tot_pw():
    while(1):
        print("Getting Total Power")
        for device in Devices.query.all():
            total_power(device)
        sleep(int(10*60))

def resources_check():
    while(1):
        print("Getting Device Resources")
        ping_devices()
        sleep(int(device_ping))

Thread(target=resources_check).start()
Thread(target = NetScan).start()
Thread(target=dev_tot_pw).start()
