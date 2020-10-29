
from flask import render_template, url_for, request, redirect, make_response, flash, send_file, url_for, redirect, request
from mirpi import app, db, bcrypt
from mirpi.forms import UserRegForm, UserLoginForm, DeviceTemplate, DeviceUpdateTemplate
from mirpi.models import User, Devices, Hubs
from flask_login import login_user, current_user, logout_user, login_required


# Title:     Dashboard Handler
# Desc:      Handler Function for Dashboard
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/", methods=['GET', 'POST'])
@app.route("/dashboard", methods=['GET', 'POST'])
def home_page():
    device = Hubs.query.all()
    count = 0
    for i in device:
        count = i.graph + count
    return render_template('dashboard.html', device=device, count=count)

# Title:     User Registration
# Desc:      User Registration Handler
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/registration", methods=['GET', 'POST'])
def user_registration():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = UserRegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created', 'success')
        return redirect(url_for('user_login'))
    return render_template('/user/user_registration.html', title='Registration', form=form)

# Title:     User Login Handler
# Desc:      User Login Handler
# Author:    JJ MAREE
# Last Mod:  01-07-2020


@app.route("/login", methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Email / Password Invalid', 'danger')
    return render_template('/user/user_login.html', title='Login', form=form)


# Title:     User Logout
# Desc:      User Logout
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('home_page'))


# Title:     About Page
# Desc:      References (Unimplemented Page / Placeholder)
# Author:    JJ MAREE
# Last Mod:  01-07-2020
@app.route("/about", methods=['GET', 'POST'])
def about_references():
    return render_template('about_references.html', title='About')
