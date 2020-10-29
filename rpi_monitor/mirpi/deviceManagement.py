    # ----------------------------------------------------------------------------------------------
#    Package Imports
# ----------------------------------------------------------------------------------------------
from mirpi.models import Devices, Sensors, NewDevices, Preferences, Power, Hubs
from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request, jsonify
from mirpi.forms import UserRegForm, UserLoginForm, DeviceTemplate, DeviceUpdateTemplate
from datetime import datetime
from mirpi import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, update
import os
import random
import csv
from time import sleep
from mirpi.emailServer import NewDeviceAdded
import mirpi.cnst as const
from mirpi.user_functions import sshInit, sshClient
from mirpi.mqttHandle import  hubControl

# ----------------------------------------------------------------------------------------------
#    Global Variables
# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------
#    User Functions
# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------
#   Web Page Routes
# ----------------------------------------------------------------------------------------------

# Title:     Device Management
# Desc:      Dashboard of all connected devices and their stats
# Author:    JJ MAREE
# Last Mod:  01-07-2020


@app.route("/network/devices", methods=['GET', 'POST'])
@login_required
def dev_man():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        devices = Devices.query.order_by(
            Devices.date_added.desc()).paginate(page=page, per_page=60)
        return render_template('/network/client_device/device_dashboard.html', title='Devices', devices=devices)
    elif request.method == 'POST':
        try:
            result = int(request.form['text_box'])
            button = request.form['submit_button']
            if button == "Power On":
                try:
                    devices = Devices.query.filter_by(
                        status="Powered Off").limit(result)
                    print(devices)
                    try:
                        for i in devices:
                            hub = Hubs.query.get_or_404(i.hub)
                            hubControl(hub, 1, i.hub_location)
                            i.state = "Idle"
                        flash("  Devices Powered On", 'success')
                    except Exception as e:
                        print(e)
                except:
                    pass
            elif button == "Power Off":
                try:
                    device = Devices.query.filter(or_(Devices.status == 'Idle', Devices.status == 'Active')).limit(result)
                    try:
                        for i in device:
                            Thread(target = devShutdown, args=(i.id)).start()
                        flash("  Devices Powered Off", 'success')
                    except Exception as e:
                        print(e)
                except:
                    pass
            return redirect(url_for('dev_man'))
        except:
            flash("  Incorrect Format", 'danger')
            return render_template('/network/client_device/device_dashboard.html', title='Devices', devices=devices)


# Title:     Device Add
# Desc:      Form to Add new Device Manually
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/add", methods=['GET', 'POST'])
@login_required
def add_dev():
    form = DeviceTemplate()
    if form.validate_on_submit():
        try:
            if(len(Hubs.query.get_or_404(form.hub.data).devices) > 8):
                hubLoc = None
                flash('Error Assigning Device to Hub', 'danger')
            else:
                hubLoc = form.hub_location.data
        except Exception as e:
            print(e)
            hubLoc = None
            flash('Error Assigning Device to Hub', 'danger')
        finally:
            hold_1 = form.hub.data
            if(hold_1 == 0):
                hold_1 = None

            device = Devices(name=form.name.data,
                             hostname=form.hostname.data,
                             username=form.username.data,
                             hub=hold_1,
                             hub_location=hubLoc,
                             ip=form.ip.data,                             
                             mac=form.mac.data
                             )
            if form.copyssh.data:
                state = sshInit(form.username.data, form.ip.data, form.password.data)
                if(state == 0):   
                    device.initiated = "1"
                    device.last_accessed = datetime.utcnow()
                    flash("  Certificates Copied", 'success')                            
                else:
                    flash("  Device Inaccessible", 'danger')
                    device.initiated = "0"
            flash('Device Added', 'success')
            db.session.add(device)
            if Preferences.query.first().new_device_added:
                try:
                    NewDeviceAdded(Preferences.query.first().email, form.ip.data, form.mac.data, form.hub.data,
                                   form.hub_location.data, form.username.data, datetime.utcnow(), form.hostname.data)
                except Exception as e:
                    print(e)
            try:
                db.session.commit()
                flash('Device Added', 'success')
                return redirect(url_for('dev_man'))
            except:
                flash('Error Assigning Device to Hub', 'danger')
                return redirect(url_for('dev_man'))
    form.hub.data = 0
    form.hub_location.data = 0
    return render_template('/network/client_device/device_config.html', title='Add Device', form=form, legend='Create Device')


# Title:     Device Modify
# Desc:      Form to Modify Device Manually
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/modify", methods=['GET', 'POST'])
@login_required
def mod_dev(dev_id):
    device = Devices.query.get_or_404(dev_id)
    form = DeviceUpdateTemplate()
    if form.validate_on_submit():
        try:
            if(len(Hubs.query.get_or_404(form.hub.data).devices) > 9):
                hubLoc = None
                flash('Error Assigning Device to Hub', 'danger')
            else:
                hubLoc = form.hub_location.data
        except Exception as e:
            print(e)
            hubLoc = None
            flash('Error Assigning Device to Hub', 'danger')
        finally:
            hold_1 = form.hub.data
            if(hold_1 == 0):
                hold_1 = None
        device.name = form.name.data
        device.hostname = form.hostname.data
        device.ip = form.ip.data
        device.mac = form.mac.data
        device.hub_location = form.hub_location.data
        device.username = form.username.data
        if form.copyssh.data:
            state = sshInit(form.username.data, form.ip.data, form.password.data)
            if(state == 0):   
                device.initiated = "1"
                device.last_accessed = datetime.utcnow()
                flash("  Certificates Copied", 'success')                            
            else:
                flash("  Device Inaccessible", 'danger')
                device.initiated = "0"
        try:
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            try:
                device.hub = form.hub.data
                db.session.commit()
            except Exception as e:
                print(e)
            return redirect(url_for('dev_man'))
    elif request.method == 'GET':
        form.name.data = device.name
        form.hostname.data = device.hostname
        form.ip.data = device.ip
        form.mac.data = device.mac
        form.hub_location.data = device.hub_location
        form.hub.data = device.hub
        form.username.data = device.username
    return render_template('/network/client_device/device_config.html', title='Modify Device', form=form, legend='Update Device')




# Title:     Device Delete
# Desc:      Form to Delete Device Manually
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/delete", methods=['GET', 'POST'])
@login_required
def del_dev(dev_id):

    device = Devices.query.get_or_404(dev_id)
    db.session.delete(device)
    db.session.commit()
    flash('Device Deleted', 'success')
    return redirect(url_for('dev_man'))


# Title:     Device CSV Import
# Desc:      Handler Used to automatically import CSV files
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route('/network/devices/add/csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in const.ALLOWED_EXTENSIONS
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Invalid File Requested', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No File Selected', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(int(random.uniform(0, 99999999)))[0:10] + ".csv"
            file.save(os.path.join(const.TEMP, filename))
            try:
                data = list(csv.reader(open(const.TEMP + filename)))
                for x in range(len(data)):
                    if x > 0:                 
                        try:
                            if(len(Hubs.query.get_or_404(int(data[x][5])).devices) > 8):
                                hubLoc = None
                                flash('Error Assigning Device to Hub', 'danger')
                            else:
                                hubLoc = data[x][5]
                        except Exception as e:
                            print(e)
                            hubLoc = None
                            flash('Error Assigning Device to Hub', 'danger')    
                        device = Devices(name=data[x][0],
                                         hostname=data[x][1],
                                         username=data[x][3],
                                         hub=hubLoc,
                                         ip=data[x][2],
                                         date_added=datetime.utcnow(),
                                         mac=data[x][8],
                                         hub_location=data[x][9],
                                         )
                        if data[x][6] == '1':
                            state = sshInit(data[x][3], data[x][2], data[x][4])
                            if(state == 0):   
                                device.initiated = "1"
                                device.last_accessed = datetime.utcnow()
                                flash("  Certificates Copied", 'success')                            
                            else:
                                flash("  Device Inaccessible", 'danger')
                                device.initiated = "0"
                        db.session.add(device)
                        db.session.commit()
                flash('CSV Imported', 'success')
            except Exception as e:
                print(e)
            finally:
                try:
                    os.remove(const.TEMP + filename)
                except Exception as e:
                    print(e)
            return redirect(url_for('dev_man'))
        else:
            flash('Incorrect File Format', 'warning')
    return render_template('/network/client_device/csv_add.html', title='Import CSV', legend='Import CSV')


# Title:     New Scanned - ADD
# Desc:      Handler that redirects user from newly scanned device to Add / Modify prev Device
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/scanned/device", methods=['GET', 'POST'])
@login_required
def new_device_found(dev_id):
    device_hold = NewDevices.query.get_or_404(dev_id)
    form = DeviceUpdateTemplate()

    if form.validate_on_submit():
        try:
            if(len(Hubs.query.get_or_404(int(data[x][5])).devices) > 8):
                hubLoc = None
                flash('Error Assigning Device to Hub', 'danger')
            else:
                hubLoc = form.hub.data
        except Exception as e:
            print(e)
            hubLoc = None
        if device_hold.new == 1:
            hold = Devices(name=form.name.data,
                           hostname=form.hostname.data,
                           ip=form.ip.data,
                           mac=form.mac.data,
                           hub_location=form.hub_location.data,
                           hub=hubLoc,
                           username=form.username.data,
                           )
            if form.copyssh.data:
                state = sshInit(form.username.data, form.ip.data, form.password.data)
                if(state == 0):   
                    device.initiated = "1"
                    device.last_accessed = datetime.utcnow()
                    flash("  Certificates Copied", 'success')                            
                else:
                    flash("  Device Inaccessible", 'danger')
                    device.initiated = "0"
            try:
                NewDevices.query.filter_by(mac=form.mac.data).delete()
            except:
                pass
            if Preferences.query.first().new_device_added:
                try:
                    NewDeviceAdded(Preferences.query.first().email, form.ip.data, form.mac.data, form.hub.data,
                                   form.hub_location.data, form.username.data, datetime.utcnow(), form.hostname.data)
                except Exception as e:
                    print(e)
            flash("  New Device Added", 'success')
            db.session.add(hold)
            db.session.commit()
        else:
            device = Devices.query.filter((Devices.ip == device_hold.ip) | (
                Devices.mac == device_hold.mac)).first()
            device.name = form.name.data
            device.hostname = form.hostname.data
            device.ip = form.ip.data
            device.mac = form.mac.data
            device.hub_location = form.hub_location.data
            device.hub = hubLoc
            device.username = form.username.data
            if form.copyssh.data:
                state = sshInit(form.username.data, form.ip.data, form.password.data)
                if(state == 0):   
                    device.initiated = "1"
                    device.last_accessed = datetime.utcnow()
                    flash("  Certificates Copied", 'success')                            
                else:
                    flash("  Device Inaccessible", 'danger')
                    device.initiated = "0"              
            try:
                NewDevices.query.filter_by(mac=form.mac.data).delete()
            except:
                pass
            if Preferences.query.first().new_device_added:
                try:
                    NewDeviceAdded(Preferences.query.first().email, form.ip.data, form.mac.data, form.hub.data,
                                   form.hub_location.data, form.username.data, datetime.utcnow(), form.hostname.data)
                except Exception as e:
                    print(e)
            flash("  Device Updated", 'success')
            db.session.commit()
        return redirect(url_for('backup_alerts'))
    elif request.method == 'GET':
        if device_hold.new == 1:
            form.ip.data = device_hold.ip
            form.mac.data = device_hold.mac
        else:
            device = Devices.query.filter((Devices.ip == device_hold.ip) | (
                Devices.mac == device_hold.mac)).first()
            form.name.data = device.name
            form.hostname.data = device.hostname
            form.ip.data = device_hold.ip
            form.mac.data = device_hold.mac
            form.hub_location.data = device.hub_location
            form.hub.data = device.hub
            form.username.data = device.username
    return render_template('/network/client_device/device_config.html', title='Add Found Device', form=form, legend='Add New Device')


# Title:     New Scanned - DELETE
# Desc:      Handler that deletes newly Scanned Device
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/network/devices/<dev_id>/scanned/delete", methods=['GET', 'POST'])
@login_required
def new_device_found_del(dev_id):
    device = NewDevices.query.get_or_404(dev_id)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('backup_alerts'))