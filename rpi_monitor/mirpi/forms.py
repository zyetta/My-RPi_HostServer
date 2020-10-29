from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, IPAddress, MacAddress
from mirpi.models import User, Devices


class UserRegForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Join')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Taken')


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DeviceTemplate(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=1, max=100)])
    hostname = StringField('Hostname', validators=None)
    ip = StringField('IP Address', validators=[DataRequired(),  IPAddress()])
    submit = SubmitField('Add Device')
    mac = StringField('MAC Address', validators=None)
    username = StringField('Device ROOT Username', validators=None)
    password = PasswordField('Device ROOT Password', validators=None)
    hub = IntegerField('Hub ID', validators=None)
    hub_location = IntegerField('Hub Pin', validators=None)
    copyssh = BooleanField('Test Device Connection')

    def validate_name(self, name):
        user = Devices.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Name Already Taken')

    def validate_ip(self, ip):
        user = Devices.query.filter_by(ip=ip.data).first()
        if user:
            raise ValidationError('IP Address Already Taken')


class HubTemplate(FlaskForm):
    ip = StringField('IP Address', validators=[DataRequired(),  IPAddress()])
    mac = StringField('MAC Address', validators=None)
    submit = SubmitField('Save')

    def validate_ip(self, ip):
        user = Devices.query.filter_by(ip=ip.data).first()
        if user:
            raise ValidationError('IP Address Already Taken')


class DeviceUpdateTemplate(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=1, max=100)])
    hostname = StringField('Hostname', validators=[
                           DataRequired(), Length(min=1, max=100)])
    ip = StringField('IP Address', validators=[DataRequired(),  IPAddress()])
    submit = SubmitField('Add Device')
    mac = StringField('MAC Address', validators=None)
    username = StringField('Device ROOT Username', validators=None)
    password = PasswordField('Device ROOT Password', validators=None)
    hub = IntegerField('Hub ID', validators=None)
    hub_location = IntegerField('Hub Pin', validators=None)
    color = StringField('Color (HEX)', validators=None)
    copyssh = BooleanField('Test Device Connection')


class PreferencesTemplate(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_scanned = BooleanField('New Device Found From Scan')
    new_device_added = BooleanField('New Device Added')
    temp_exceeded = BooleanField('Temperature Limit Exceeded')
    curr_exceeded = BooleanField('Current Limit Exceeded')
    database_backup = BooleanField('Database Backup')
    shutdown_all = BooleanField('Shutdown All Devices')
    curr_upper = DecimalField(
        'Upper, Active Current Limit', validators=[DataRequired()])
    curr_lower = DecimalField(
        'Lower, Active Current Limit', validators=[DataRequired()])
    curr_max = DecimalField('Maximium Current Limit',
                            validators=[DataRequired()])
    temp_max = DecimalField('Maximium Temperature',
                            validators=[DataRequired()])
    net_scan = StringField('Network Scan Address', validators=[DataRequired()])
    status_threash = DecimalField('Activity Threshold for Powered Status [%]',
                            validators=[DataRequired()])
    submit = SubmitField('Save')
