from mirpi.models import Devices, Sensors, NewDevices, Preferences, Power, Hubs
from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request, jsonify
from mirpi.forms import UserRegForm, UserLoginForm, DeviceTemplate, DeviceUpdateTemplate
from datetime import datetime
from mirpi import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
import os
import paramiko
import subprocess
import random
import nmap
import threading
import csv
from time import sleep
from mirpi.emailServer import NewDeviceAdded
from mirpi.globalVariables import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from mirpi.user_functions import sshInit, sshClient
from mirpi.mqttHandle import Hub_Init, Hub_Control


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



