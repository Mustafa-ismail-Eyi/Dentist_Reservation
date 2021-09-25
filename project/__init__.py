from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import session
from flask_socketio import SocketIO, emit

# This is the main application
app = Flask(__name__)
# every app needs its own secret key
app.config['SECRET_KEY'] = 'mysecretkey'

# app configurations for database connection and database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:365478@localhost:5432/Dental_Reservation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Binding app with SQLAlchemy
db = SQLAlchemy(app)
# Migrating
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'patients.login_patient'

socketio = SocketIO(app)

from project.patients.views import patients
from project.core.views import core
from project.reservations.views import reservations
from project.dent.views import dent
app.register_blueprint(patients)
app.register_blueprint(core)
app.register_blueprint(reservations)
app.register_blueprint(dent)

