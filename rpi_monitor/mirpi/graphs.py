from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request, Response
import json
from mirpi import app, db, engine
from mirpi.forms import DeviceTemplate, DeviceUpdateTemplate
from mirpi.models import Devices, Sensors, Power, Hubs
from mirpi.user_functions import devResourceSample
from threading import Thread


# Title:     Live Sensor Data Plot
# Desc:      Initlizes the live chart that sensor data will be shown on
# Author:    JJ MAREE
# Last Mod:  06-07-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: JSON Response of Sensor Data
@app.route("/data/live", methods=['GET', 'POST'])
def liveCharts():
    i = 0
    a = [[]]
    for device in Hubs.query.filter_by(graph=1):
        unix = []
        voltage = []
        current = []
        temperature = []
        pw = []
        data = Sensors.query.filter_by(hub_id=device.id).order_by(
            Sensors.unix.desc()).limit(50)
        data = data[::-1]
        try:
            rows = 0
            for rows in data:
                unix.append(rows.unix * 1000)
                voltage.append([rows.unix * 1000, round(rows.volt, 2)])
                current.append([rows.unix * 1000, round(rows.curr, 2)])
                temperature.append([rows.unix * 1000, round(rows.temp, 2)])
                pw.append([rows.unix * 1000, round(rows.curr * rows.volt, 2)])
                device.unix_token = rows.unix

            if rows != 0:
                db.session.commit()
                a.insert(i, [{"name": device.id, "data": temperature, "lineWidth": 2, "fillOpacity": 1, "marker": {"radius": 1}},
                             {"name": device.id, "data": current, "lineWidth": 2,
                                 "fillOpacity": 1, "marker": {"radius": 1}},
                             {"name": device.id, "data": voltage, "lineWidth": 2,
                                 "fillOpacity": 1, "marker": {"radius": 1}},
                             {"name": device.id, "data": pw},
                             ])
        except Exception as e:
            print(e)

        finally:
            i = i + 1
    response = make_response(json.dumps(a))
    response.content_type = 'application/json'
    return response


# Title:     Updates Live Chart
# Desc:      Passes sensor data to the chart to update
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: JSON Response of Sensor Data (Update)
@app.route("/data/update", methods=['GET', 'POST'])
def updateCharts():
    i = 0
    a = [[]]
    for device in Hubs.query.filter_by(graph=1):
        data = Sensors.query.filter(device.unix_token < Sensors.unix).filter_by(
            hub_id=device.id).order_by(Sensors.unix.desc())
        data = data[::-1]
        unix = []
        voltage = []
        current = []
        temperature = []
        pw = []
        rows = 0
        for rows in data:
            unix.append(rows.unix * 1000)
            voltage.append([rows.unix * 1000, round(rows.volt, 2)])
            current.append([rows.unix * 1000, round(rows.curr, 2)])
            temperature.append([rows.unix * 1000, round(rows.temp, 2)])
            pw.append([rows.unix * 1000, round(rows.curr * rows.volt, 2)])
        if rows != 0:
            a.insert(i, [temperature,
                         current,
                         voltage,
                         pw])
            device.unix_token = rows.unix
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        i = i + 1
    response = make_response(json.dumps(a))
    response.content_type = 'application/json'
    return response


# Title:     Update Stats
# Desc:      Updates the graph displaying the number of active devices
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: JSON Response of Device States
@app.route('/data/stats', methods=["GET", "POST"])
def deviceStates():
    a = [[]]
    status = []
    added = 0
    registered = 0
    try:
        for device in Devices.query.all():
            status.append(device.status)
    except Exception as e:
        print(e)
    finally:
        a.insert(0, [{"Active": status.count('Active'), "Idle": status.count(
            'Idle'), "Off": status.count('Powered Off')}])
        response = make_response(json.dumps(a))
        response.content_type = 'application/json'
        return response

# Title:     Ping Devices
# Desc:      Pings the devices to to determine their current status
# Author:    JJ MAREE
# Last Mod:  01-05-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: None
@app.route('/data/ping', methods=["GET", "POST"])
def pingDevices():
    try:
        Thread(target = devResourceSample).start()
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for('dev_man'))

# Title:     Device Resource usage
# Desc:      Chart Showing Device Resource usage
# Author:    JJ MAREE
# Last Mod:  01-07-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: JSON Response of device resource usage

@app.route("/data/device/resources", methods=['GET', 'POST'])
def deviceResource():
    i = 0
    a = [[]]
    try:
        for device in Devices.query.all():
            CPU = device.cpu_usage
            RAM = round(device.memory_usage / 1000000, 2)
            NAME = device.name + " | " + device.mac + \
                " <br> Last Accessed: " + str(device.last_accessed)
            a.insert(i, [CPU, RAM, NAME])
            i = i + 1
    except Exception as e:
        print(e)
    finally:
        response = make_response(json.dumps(a))
        response.content_type = 'application/json'
        return response

# Title:     Total Power Consumption
# Desc:      Chart Showing Device Total Power Consumption
# Author:    JJ MAREE
# Last Mod:  01-07-2020
# --------------------------------------------------------------------
# Parameters: None
# Return: JSON Response of longterm Power usage

@app.route("/data/device/")
def totalPowerCharts():
    try:
        a = [[]]
        for device in Hubs.query.filter_by(graph=1).all():
            pw = []
            try:
                for i in Power.query.filter_by(device_id=device.id).all():
                    pw.append([i.unix * 1000, round(i.power, 2)])
            except Exception as e:
                print(e)
            finally:
                a.insert(
                    1, [{"name": str(device.id) + " | " + str(device.mac), "data": pw}])
    except Exception as e:
        print(e)
    finally:
        response = make_response(json.dumps(a))
        response.content_type = 'application/json'
        return response
