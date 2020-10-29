import pandas as pd
import numpy as np
import calendar
import time
import os
import paramiko
import nmap
import mirpi.cnst as const

from mirpi.models import Power, Sensors, Preferences, Devices, Hubs, NewDevices
from mirpi.emailServer import NewFound
from datetime import datetime, date
from mirpi import engine, db


# Title:     Total Power Calculator
# Author:    JJ MAREE
# Last Mod:  07-07-2020
# -----------
# Input: Hub ID
# Return: None
# Funtion: Resamples total sensor data, sorting it by device ID and month.

def totalPower(device):
    pw = []
    sensor_df = pd.read_sql(
        "SELECT * FROM sensors where hub_id =  %(uid)s", engine, params={"uid": device.id})
    try:
        device.samples_stored = len(sensor_df['unix'])
        s_temp = pd.DataFrame(columns=['power', 'date_added'])
        s_temp['power'] = sensor_df['curr'] * sensor_df['volt']
        s_temp['date_added'] = pd.to_datetime(sensor_df['unix'], unit='s')
        s = s_temp.resample('M', on='date_added')['power'].sum()
        uni_time = s.index.to_numpy()
        value = s.to_numpy()
        if value:
            for i in range(len(value)):
                t_hold = (
                    uni_time[i] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
                entry = Power.query.filter_by(device_id=device.id, unix=int(
                    t_hold)).first()  # Check if Entry Exists

                if entry:
                    try:
                        entry.power = float(value[i])
                        db.session.commit()
                    except:
                        print("Err. Rollback")
                        db.session.rollback()
                else:
                    try:
                        entry_hold = Power(
                            unix=int(t_hold), device_id=device.id, power=float(value[i]))
                        db.session.add(entry_hold)
                        db.session.commit()
                    except:
                        print("Err 2. Rollback")
                        db.session.rollback()
        else:
            try:
                d2 = date.today().replace(day=calendar.monthrange(
                    date.today().year, date.today().month)[1])
                t_hold = time.mktime(d2.timetuple()) * 1000
                entry_hold = Power(
                    unix=int(t_hold), device_id=device.id, power=0)
                db.session.add(entry_hold)
                db.session.commit()
            except:
                print("Err. Rollback")
                db.session.rollback()
    except Exception as e:
        print(e)



# Title:     Ping Devices
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# -----------
# Input: None
# Return: None
# Funtion: SSH'es into each accessible device, and samples resource usage.
def devResourceSample():
    for device in Devices.query.all():
        try:
            if (device.initiated == '1'):
                response = os.system("ping -c 1 " + device.ip)
                if(response == 0):
                    print("Accessing: " + str(device.ip))
                    ssh_client(device.username, device.ip,
                            "python3 ./control/resource_check.py &")
                else:
                    device.status = 'Powered Off'
                    device.cpu_usage = 0
                    device.memory_usage = 0
                    db.session.commit()
        except Exception as e:
            print(e)

# Title:     Initiation Process
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# -----------
# Input: Device username, ip/hostname, password
# Return: None
# Funtion: SSH into device, initiates certificates, transfers dependent files, and installs required packages.
def sshInit(user, server, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(server, username=user, password=password)
        ssh.exec_command("mkdir -p .ssh")
        ssh.exec_command("mkdir -p control")
        ftp_client = ssh.open_sftp()
        ftp_client.put(const.CERT, '.ssh/mirpi.pub')
        ftp_client.put(const.LEDFILE, 'control/shutdown_script.py')
        ftp_client.put(const.PINGFILE, 'control/resource_check.py')
        ftp_client.put('./mirpi/rpi/deployment.sh', 'control/deployment.sh')
        ssh.exec_command("cat .ssh/mirpi.pub >> .ssh/authorized_keys")
        ssh.exec_command("chmod 600 .ssh/*")
        ssh.exec_command("sudo sh control/deployment.sh &")    
        ftp_client.close()
        ssh.close()
        return 0
    except Exception as e:
        return 1


# Title:     SSH Client w/ Public Keys
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# -----------
# Input: Device username, ip/hostname, command to execute.
# Return: None
# Funtion: SSH client that is able to access device with the use of  a private key.
def sshClient(user, server, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(server, username=user, key_filename=const.CERTPVT)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.readlines()
        ssh.close()
    except Exception as e:
        print(e)

# Title:     Network Scanner
# Author:    JJ MAREE
# Last Mod:  01-07-2020
# -----------
# Input: None
# Return: None
# Funtion: Background Loop that continually scans  for network changes.

def NetScan():
    while(1):
        network = str(Preferences.query.get_or_404(1).net_scan)
        nm = nmap.PortScanner()
        nm.scan(hosts=network, arguments='-sn')
        host_list = []
        print("Scanning Network")
        for i in nm.all_hosts():
            address = nm[i]['addresses']
            try:
                mac_hold = address['mac']
            except:
                mac_hold = None
            try:
                ipv4_hold = address['ipv4']
            except:
                ipv4_hold = None
            host_list.append([mac_hold, ipv4_hold])
        for i in host_list:
            try:
                device = None
                hold = None
                ip_hold = str(i[1])
                mac_hold = str(i[0])
                update = 0
                if ((i[0] == None) & ((i[1] != None))):  # No Mac, But IPV4
                    print("No Mac, But IPV4")
                elif ((i[0] != None) & ((i[1] == None))):  # Mac, But No IPV4
                    print("Mac, But No IPV4")
                elif ((i[0] != None) & ((i[1] != None))):
                    #Mac and IPV4
                    if (Devices.query.filter_by(ip=ip_hold, mac=mac_hold).first()):
                        pass
                    elif (NewDevices.query.filter_by(ip=ip_hold, mac=mac_hold).first()):
                        pass
                    elif (Hubs.query.filter_by(ip=ip_hold, mac=mac_hold).first()):
                        pass
                    elif (Devices.query.filter((Devices.ip == ip_hold) | (Devices.mac == mac_hold)).first()):
                        hold = NewDevices(mac=mac_hold,
                                          ip=ip_hold,
                                          date_added=datetime.utcnow(),
                                          new=0)
                        update = 0
                    elif (NewDevices.query.filter((NewDevices.ip == ip_hold) | (NewDevices.mac == mac_hold)).first()):
                        hold = NewDevices(mac=mac_hold,
                                          ip=ip_hold,
                                          date_added=datetime.utcnow(),
                                          new=1)
                        update = 1

                    elif (Hubs.query.filter((Hubs.ip == ip_hold) | (Hubs.mac == mac_hold)).first()):
                        hold = NewDevices(mac=mac_hold,
                                          ip=ip_hold,
                                          date_added=datetime.utcnow(),
                                          new=0)
                        update = 0
                    else:
                        hold = NewDevices(mac=mac_hold,
                                          ip=ip_hold,
                                          date_added=datetime.utcnow(),
                                          new=1)
                        update = 1
                    print("MAC and IPV4")
                if hold:
                    try:
                        if Preferences.query.first().new_scanned:
                            try:
                                NewFound(Preferences.query.first(
                                ).email, ip_hold, mac_hold, update, datetime.utcnow())
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                try:
                    db.session.add(hold)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
            except Exception as e:
                print(e)
        time.sleep(const.netScanTime)
