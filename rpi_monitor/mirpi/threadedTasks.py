from mirpi.user_functions import totalPower, NetScan, devResourceSample
from threading import Thread
from mirpi.models import Devices, Hubs
from time import sleep
import mirpi.cnst as const

# Title:     Device State
# Desc:      Threaded Loop to capture Device resource usage [RAM / CPU / ETC]
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def resourceSample():
    while(1):
        print("Getting Device Resources")
        ping_devices()
        sleep(int(const.pingPeriod))


# Title:     Total Power Consumption
# Desc:      Threaded Loop to capture Total Power Consumption
# Author:    JJ MAREE
# Last Mod:  01-07-2020

def totalPowerLoop():
    while(1):
        print("Getting Total Power")
        for device in Hubs.query.all():
            totalPower(device)
        sleep(int(const.totPowerSamp))


Thread(target = resourceSample).start()
Thread(target = NetScan).start()
Thread(target = totalPowerLoop).start()

