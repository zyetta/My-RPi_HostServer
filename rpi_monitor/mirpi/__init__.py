from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine
from datetime import datetime
import atexit
from sqlalchemy import create_engine
import mirpi.cnst as const


app = Flask(__name__)
app.secret_key = 'bm9W4P87tOzT$yLt!Cg4EJ3eEl$sdyJBkrqh93sWw&2mlMo'
app.config['SECRET_KEY'] = 'b36e50a789cee54e70e6359e8881b3ec'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + const.mysql_user + ':' + const.mysql_password + '@' + const.mysql_server + '/' + const.mysql_table
engine = create_engine('mysql+pymysql://' + const.mysql_user + ':' + const.mysql_password + '@' + const.mysql_server + '/' + const.mysql_table,echo=False)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
login_manager.login_message_category = 'info'

from mirpi import models
from mirpi import preferences
from mirpi import routes
from mirpi import graphs
from mirpi import deviceManagement
from mirpi import hubManagement
from mirpi import threadedTasks