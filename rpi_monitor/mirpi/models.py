from mirpi import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(16020), nullable=False)


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    hostname = db.Column(db.String(120), nullable=True)
    ip = db.Column(db.String(20), nullable=False)
    mac = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20))
    cpu_usage = db.Column(db.REAL, nullable=True)
    memory_usage = db.Column(db.REAL, nullable=True)
    memory_total = db.Column(db.REAL, nullable=True)
    cpu_temp = db.Column(db.REAL, nullable=True)
    username = db.Column(db.String(120), nullable=True)
    pin_init_time = db.Column(db.DateTime, default=datetime.utcnow())
    pin_init = db.Column(db.Integer, nullable=True, default='0')
    initiated = db.Column(db.String(20))
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow())
    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    hub = db.Column(db.Integer, db.ForeignKey('hubs.id'), nullable=True)
    hub_location = db.Column(db.Integer, nullable=True, default='0')


class Hubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graph = db.Column(db.Integer, nullable=True, default='0')
    ip = db.Column(db.String(20), nullable=True)
    mac = db.Column(db.String(20), nullable=True)
    sensor_post = db.relationship('Sensors', backref='author')
    total_pw = db.relationship('Power', backref='author')
    samples_stored = db.Column(db.Integer, nullable=True)
    unix_token = db.Column(db.Integer, nullable=True)
    devices = db.relationship(
        'Devices', backref=db.backref('author', lazy=True))


class NewDevices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(20), nullable=True)
    ip = db.Column(db.String(20), nullable=True)
    date_added = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow())
    new = db.Column(db.Integer, nullable=False)


class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=True, default='')
    new_scanned = db.Column(db.Integer, nullable=True, default='1')
    new_device_added = db.Column(db.Integer, nullable=True, default='1')
    temp_exceeded = db.Column(db.Integer, nullable=True, default='1')
    curr_exceeded = db.Column(db.Integer, nullable=True, default='1')
    shutdown_all = db.Column(db.Integer, nullable=True, default='1')
    loadshedding = db.Column(db.Integer, nullable=True, default='1')
    broker_connected = db.Column(db.Integer, nullable=True, default='0')
    date_connected = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    curr_upper = db.Column(db.REAL, nullable=False, default=1.5)
    curr_lower = db.Column(db.REAL, nullable=False, default=1.4)
    curr_max = db.Column(db.REAL, nullable=False, default=3)
    temp_max = db.Column(db.REAL, nullable=False, default=65)
    status_threash = db.Column(db.REAL, nullable=False, default=65)
    net_scan = db.Column(db.String(20), nullable=True,
                         default="192.168.137.1/24")


class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unix = db.Column(db.Integer, nullable=False)
    curr = db.Column(db.REAL, nullable=True)
    volt = db.Column(db.REAL, nullable=True)
    temp = db.Column(db.REAL, nullable=True)
    hub_id = db.Column(db.Integer, db.ForeignKey(
        'hubs.id'), nullable=False)


class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    power = db.Column(db.REAL, nullable=False)
    unix = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey(
        'hubs.id'), nullable=False)


db.create_all()


def first_run():
    hold = Preferences()
    db.session.add(hold)
    db.session.commit()


if not Preferences.query.first():
    first_run()
