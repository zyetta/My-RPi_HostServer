from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from mirpi import app, db, bcrypt
from mirpi.forms import UserRegForm, UserLoginForm, DeviceTemplate, DeviceUpdateTemplate, PreferencesTemplate
from mirpi.models import User, Devices, Preferences, Sensors, NewDevices
import os
import json
from email.message import EmailMessage
from mirpi.hubManagement import shutdown_dev
from mirpi.emailServer import testMail, ShutdownAll


# Title:     Preferences Form
# Desc:      Form that will handle all Preferences information
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/preferences", methods=['GET', 'POST'])
@login_required
def backup_alerts():
    pref = Preferences.query.get_or_404(1)
    device_hold = NewDevices.query.all()
    form = PreferencesTemplate()
    if request.method == "POST":
        if request.form['submit_button'] == 'Test Email':
            if form.email.data != "":
                try:
                    testMail(form.email.data)
                except:
                    flash("  Failed to Send", 'danger')
                else:
                    flash("  Email Sent", 'success')
                return render_template('preferences.html', title='Preferences', form=form, legend="Preferences", pref=pref, device=device_hold)
            else:
                flash("  No Address Entered", 'warning')
                return render_template('preferences.html', title='Preferences', form=form, legend="Preferences", pref=pref, device=device_hold)
        elif request.form['submit_button'] == 'Save Preferences':
            pref.new_scanned = int(form.new_scanned.data)
            pref.new_device_added = int(form.new_device_added.data)
            pref.temp_exceeded = int(form.temp_exceeded.data)
            pref.curr_exceeded = int(form.curr_exceeded.data)
            pref.database_backup = int(form.database_backup.data)
            pref.shutdown_all = int(form.shutdown_all.data)
            pref.status_threash = float(form.status_threash.data)
            pref.curr_upper = float(form.curr_upper.data)
            pref.curr_lower = float(form.curr_lower.data)
            pref.curr_max = float(form.curr_max.data)
            pref.temp_max = float(form.temp_max.data)
            pref.net_scan = form.net_scan.data

            pref.email = form.email.data
            db.session.commit()
            flash("  Settings Saved", 'success')
        elif request.form['submit_button'] == "Flush Logs":
            flash("  Logs Flushed", 'success')
            for devices in Devices.query.all():
                sensors = Sensors.query.filter_by(
                    hub_id=devices.id).delete()
                device = Devices.query.get_or_404(devices.id)
                db.session.delete(device)
                db.session.commit()
            Sensors.query.delete()
            Devices.query.delete()
            db.session.commit()
        elif request.form['submit_button'] == "Disable All Device Graphs":
            for device in Devices.query.all():
                device.graph = 0
            db.session.commit()
            flash("  Device Graphs Disabled", 'success')
            return render_template('preferences.html', title='Preferences', form=form, legend="Preferences", pref=pref, device=device_hold)
        elif request.form['submit_button'] == "Enable All Device Graphs":
            if pref.email != '':
                for device in Devices.query.all():
                    device.graph = 1
                db.session.commit()
                flash("  Device Graphs Enabled", 'success')
            else:
                flash("  No Email Entered", 'danger')
        elif request.form['submit_button'] == "Shutdown All Devices":
            try:
                flash("  Shutting Down All Deives", 'info')
                device = Devices.query.filter_by(
                    status=("Active" or "Idle")).all()
                try:
                    try:
                        if Preferences.query.first().shutdown_all:
                            try:
                                ShutdownAll(Preferences.query.first().email)
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                    for i in device:
                        shutdown_dev(i.id)
                except Exception as e:
                    print(e)
            except:
                pass
        elif request.form['submit_button'] == "Delete All Scanned Devices":
            try:
                NewDevices.query.delete()
                db.session.commit()
                flash("  Deleted All Devices in Scanned Buffer", 'success')
                device_hold = NewDevices.query.all()
                return render_template('preferences.html', title='Preferences', form=form, legend="Preferences", pref=pref, device=device_hold)
            except Exception as e:
                print(e)

        else:
            return render_template('preferences.html', title='Preferences', form=form, legend="Preferences", pref=pref, device=device_hold)
    form.email.data = pref.email
    form.new_scanned.data = pref.new_scanned
    form.new_device_added.data = pref.new_device_added
    form.temp_exceeded.data = pref.temp_exceeded
    form.curr_exceeded.data = pref.curr_exceeded
    form.shutdown_all.data = pref.shutdown_all
    form.status_threash.data = pref.status_threash
    form.curr_upper.data = pref.curr_upper
    form.curr_lower.data = pref.curr_lower
    form.curr_max.data = pref.curr_max
    form.temp_max.data = pref.temp_max
    form.net_scan.data = pref.net_scan
    return render_template('preferences.html', title='Preferences', form=form, device=device_hold, legend="Preferences", pref=pref)
