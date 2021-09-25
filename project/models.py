from datetime import date
from enum import unique
from operator import index
from datetime import datetime
from os import terminal_size

from flask.scaffold import F
from project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) < 11111111110: 
        return Patient.query.get(user_id) 
    else:
        return Dentist.query.get(user_id)

class Patient(db.Model, UserMixin):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_email = db.Column(db.String(64), unique=True, index = True)
    patient_name = db.Column(db.String(64), nullable=False)
    patient_surname = db.Column(db.String(64), nullable=False)
    patient_phone = db.Column(db.String(13), unique=True, nullable=False)
    patient_password_hash = db.Column(db.String(128), nullable=False)
    

    def __init__(self, email, name, surname, password, phone):
        self.patient_email = email
        self.patient_name = name
        self.patient_surname = surname
        self.patient_phone = phone
        self.patient_password_hash = generate_password_hash(password)
    
    
    def check_password(self,password):
        return check_password_hash(self.patient_password_hash, password)

    def get_id(self):
        return self.patient_id
class Dentist(db.Model, UserMixin):
    __tablename__ = "dentists"

    # dentist_id is the ID number on the Dentist's ID card
    dentist_id = db.Column(db.String(11), primary_key = True, unique=True)
    dentist_name_surname = db.Column(db.String(64), nullable=False)
    dentist_email = db.Column(db.String(64), unique=True, nullable = False)
    dentist_password_hash = db.Column(db.String(128), nullable = False)
    dentist_phone = db.Column(db.String(13), unique=True, nullable = False)

    def __init__(self, email, password, phone, dentist_id, dentist_name):
        self.dentist_id = dentist_id
        self.dentist_email = email
        self.dentist_password_hash = generate_password_hash(password)
        self.dentist_phone = phone
        self.dentist_name_surname = dentist_name
    
    
    def check_password(self,password):
        return check_password_hash(self.dentist_password_hash, password)

    def get_id(self):
        return self.dentist_id


class Reservations(db.Model):
    __tablename__ = "reservations"
    patients = db.relationship(Patient)
    dentist = db.relationship(Dentist)


    reservation_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    dentist_id = db.Column(db.String(11), db.ForeignKey('dentists.dentist_id'), nullable=False)
    reservation_datetime = db.Column(db.DateTime, nullable =False)
    patient_note = db.Column(db.Text, nullable = True)
    dentist_note_and_perscription = db.Column(db.Text, nullable = True)
    reservation_book_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def __init__(self, patient_id, dentist_id, date_time, patient_note, dentist_notes):
        self.patient_id = patient_id
        self.dentist_id = dentist_id
        self.reservation_datetime = date_time
        self.patient_note = patient_note
        self.dentist_note_and_perscription = dentist_notes

