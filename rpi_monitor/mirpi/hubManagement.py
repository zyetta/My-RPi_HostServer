# ----------------------------------------------------------------------------------------------
#    Package Imports
# ----------------------------------------------------------------------------------------------
from mirpi.models import Hubs, Devices, NewDevices, Sensors, Power
from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request, jsonify
from mirpi.forms import UserRegForm, UserLoginForm, HubTemplate, DeviceUpdateTemplate
from datetime import datetime
from mirpi import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from mirpi.emailServer import NewDeviceAdded
from mirpi.user_functions import sshClient
from mirpi.mqttHandle import hubInit, hubControl
import time
from threading import Thread
import mirpi.cnst as const


# ----------------------------------------------------------------------------------------------
#    Global Variables
# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------
#    User Functions
# ----------------------------------------------------------------------------------------------

 
# ----------------------------------------------------------------------------------------------
#   Web Page Routes
# ----------------------------------------------------------------------------------------------

# Title:     Hide/Show on Live Chart
# Desc:      Handler Triggered to either hide or show device on chart
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs/show", methods=['GET', 'POST'])
@login_required
def dev_upd():
    device = Hubs.query.get_or_404(request.form['id'])
    device.graph = request.form['show']
    db.session.commit()
    return jsonify({'result': 'success'})




# Title:     Hub Management
# Desc:      Dashboard of all connected hubs and their devices
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs", methods=['GET', 'POST'])
@login_required
def hub_management():
    page = request.args.get('page', 1, type=int)
    hubs = Hubs.query.order_by(Hubs.id.asc()).paginate(page=page, per_page=60)
    return render_template('/network/hub/hub_dashboard.html', title='Hubs', hubs=hubs, legend='Hub Management')


# Title:     Power off hub
# Desc:      Powers off entire hub
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def powerOffHub(device):
    hub = Hubs.query.get_or_404(device)
    devs = Devices.query.filter_by(hub = device)
    for i in range(9):
        try:
            a = devs[i]
            sshClient(a.username, a.ip, "sudo shutdown -h now &")
            time.sleep(5)
            flash('Device Shutdown Successful', 'success')
            hubControl(hub, 0, i)
        except:
            hubControl(hub, 0, i)
            flash('Error connecting to device', 'danger')
            pass


# Title:     Powers off hub function
# Desc:      Powers off all ports connected to hub
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs/<dev_id>/off", methods=['GET', 'POST'])
@login_required
def pwr_down_hub(dev_id):
    Thread(target = powerOffHub, args = (dev_id,)).start()
    return redirect(url_for('hub_management'))



# Title:     Powers on hub function
# Desc:      Powers on all ports connected to hub
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def powerOnHub(device):
    hub = Hubs.query.get_or_404(device)
    for i in range(9):
        try:
            if(hubControl(hub, 1, i)):  
                pass              
            else:
                flash('Error Sending Command', 'danger')
            time.sleep(1)
        except:
            pass



# Title:     Powers on hub
# Desc:      Powers on all ports connected to hub
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs/<dev_id>/on", methods=['GET', 'POST'])
@login_required
def pwr_up_hub(dev_id):
    hub = Hubs.query.get_or_404(dev_id)
    Thread(target = powerOnHub, args = (dev_id,)).start()
    flash('Powering On All Hubs', 'success')
    return redirect(url_for('hub_management'))




# Title:     Device Delete
# Desc:      Form to Delete Device Manually
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs/<dev_id>/delete", methods=['GET', 'POST'])
@login_required
def del_hub(dev_id):
    sensors = Sensors.query.filter_by(hub_id=dev_id).delete()
    power = Power.query.filter_by(device_id=dev_id).delete()
    hub = Hubs.query.get_or_404(dev_id)
    db.session.delete(hub)
    db.session.commit()

    flash('Hub Deleted', 'success')
    return redirect(url_for('hub_management'))


# Title:     Add Hub
# Desc:      Form to Delete Device Manually
# Author:    JJ MAREE
# Last Mod:  01-07-2020

@app.route("/network/hubs/add", methods=['GET', 'POST'])
@login_required
def add_hub():
    form = HubTemplate()
    if form.validate_on_submit():
        try:
            hub = Hubs(mac=form.mac.data,
                       ip=form.ip.data
                       )
            flash('Hub Added', 'success')
            db.session.add(hub)
            db.session.commit()
            return redirect(url_for('hub_management'))

        except Exception as e:
            flash('Error Adding Device to Hub', 'danger')
    else:
        flash('Error Adding Hub', 'danger')
        return render_template('/network/hub/hub_config.html', title='Add Device', form=form, legend='Create Device')
    return render_template('/network/hub/hub_config.html', title='Add Device', form=form, legend='Create Device')


#Title:      Modify hub
# Desc:      Modifies hub information
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/hubs/<dev_id>/modify", methods=['GET', 'POST'])
@login_required
def mod_hub(dev_id):
    form = HubTemplate()
    hub = Hubs.query.get_or_404(dev_id)
    if form.validate_on_submit():
        try:
            hub.mac=form.mac.data
            hub.ip=form.ip.data
            flash('Hub Updated', 'success')
            db.session.commit()
            return redirect(url_for('hub_management'))

        except Exception as e:
            flash('Error Adding Device to Hub', 'danger')
    elif request.method == 'GET':
        form.ip.data = hub.ip
        form.mac.data = hub.mac
        return render_template('/network/hub/hub_config.html', title='Modify Device', form=form, legend='Update Device')
    return render_template('/network/hub/hub_config.html', title='Add Device', form=form, legend='Create Device')

  
# Title:     Shutdown Device
# Desc:      Graceful Shutdown Handler
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/shutdown", methods=['GET', 'POST'])
@login_required
def shutdown_dev(dev_id):
    Thread(target = devShutdown, args = (dev_id,)).start()
    flash('Device Shutdown', 'success')
    return redirect(url_for('dev_man'))



# Title:     Shutdown Device
# Desc:      Graceful shutdown function
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def devShutdown(dev_id):
    device = Devices.query.get_or_404(dev_id)
    hub = Hubs.query.get_or_404(device.hub)
    try:
        sshClient(device.username, device.ip, "sudo shutdown -h now &")
        time.sleep(const.safeShutdown)
    except Exceotion as e:
        print(e)       
        hubControl(hub, 0, device.hub_location)
        device.state = "Powered Off"
        db.session.commit()



# Title:     Power On Device
# Desc:      Power On Device
# Author:    JJ MAREE
# Last Mod:  01-07-2020

@app.route("/network/devices/<dev_id>/poweron", methods=['GET', 'POST'])
@login_required
def poweron_dev(dev_id):
    device = Devices.query.get_or_404(dev_id)
    try:
        hub = Hubs.query.get_or_404(device.hub)
        hubControl(hub, 1, device.hub_location)
        device.state = "Idle"
        db.session.commit()
        flash('Command Executed', 'success')
    except Exception as e:
        flash('Error Executing Command', 'danger')
        print(e)
    return redirect(url_for('dev_man'))

# Title:     Initiate Hub
# Desc:      Initiates the hub, and assinges it a unique ID
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/init", methods=['GET', 'POST'])
@login_required
def hub_initiation(dev_id):
    hub = Hubs.query.get_or_404(dev_id)
    try:
        hubInit(hub)
        flash('Initiation Command Sent', 'success')
    except Exception as e:
        flash('Error Sending Command', 'danger')
        print(e)
    return redirect(url_for('hub_management'))



# Title:     New Scanned - Hub
# Desc:      Handler Function that adds new Hub
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/scanned/hub", methods=['GET', 'POST'])
@login_required
def new_hub_found(dev_id):
    device_hold = NewDevices.query.get_or_404(dev_id)
    form = HubTemplate()
    if form.validate_on_submit():
        if device_hold.new == 1:
            hold = Hubs(
                ip=device_hold.ip,
                mac=device_hold.mac
            )
            db.session.add(hold)
            db.session.commit()
            flash("  New Hub Added", 'success')
            device = NewDevices.query.get_or_404(dev_id)
            db.session.delete(device)
            db.session.commit()
            hub = Hubs.query.filter(Hubs.mac == device_hold.mac).first()
            hubInit(hub)
            return redirect(url_for('backup_alerts'))
        else:
            device = Hubs.query.filter((Hubs.ip == device_hold.ip) | (Hubs.mac == device_hold.mac)).first()
            device.ip = form.ip.data
            device.mac = form.mac.data
            db.session.commit()
            flash("  Hub Updated", 'success')
            device = NewDevices.query.get_or_404(dev_id)
            db.session.delete(device)
            db.session.commit()
    elif request.method == 'GET':
        if device_hold.new == 1:
            form.ip.data = device_hold.ip
            form.mac.data = device_hold.mac
        else:
            device = Hubs.query.filter((Hubs.ip == device_hold.ip) | ( Devices.mac == device_hold.mac)).first()
            form.ip.data = device_hold.ip
            form.mac.data = device_hold.mac
    return render_template('/network/hub/hub_config.html', title='Modify Device', form=form, legend='Update Device')