from datetime import date, datetime
from os import SEEK_CUR
from re import T
from werkzeug import datastructures
from project.models import Dentist, Patient
from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, InputRequired
from wtforms import ValidationError
from project.models import Reservations
from project import db
from sqlalchemy import text

class ReservationForm(FlaskForm):
    reservation_datetime = DateTimeField(validators=[DataRequired()], format="%Y-%m-%dT%H:%M")
    reservation_doctor_name = SelectField(choices=[""]+[dentists.dentist_name_surname for dentists in Dentist.query.filter_by()] ,validators=[InputRequired()])
    reservation_patient_note = TextAreaField()
    reservation_submit = SubmitField("Book")

    def isDateWeekDay(self,date_) -> bool:
        # 0-6 -> monday-sunday
        if 0 <= date_.weekday() <= 4:
            return True
        else:
            return False 

    def isDateValid(self, date_) -> bool:
        #if datetime.utcnow() < date_ :# if a date is valid date(not before today) which user entered
        if 0 < int((date_.date() - datetime.utcnow().date()).days) <=30:    
            # Then chek it is weekday or not
            if self.isDateWeekDay(date_):
                # check the there isn't any reservation was made before 
                 return True
            else:
                return False
        else:
            return False
    
    def isTimeValid(self, date_) -> bool:
        if  8 <= int(date_.time().hour) <= 17:
            return True
        else:
            False
    
    def isDentistAvailable(self, date_, dentist) -> bool:
        dentist_available_query = db.engine.execute(text("""SELECT r.dentist_id, r.reservation_datetime
                            FROM dentists d JOIN reservations r ON d.dentist_id = r.dentist_id
                            WHERE d.dentist_name_surname = '{dentist_name}' AND r.reservation_datetime = '{_date_}'
                            ORDER BY r.reservation_datetime DESC 
                            """.format(_date_ = date_, dentist_name = dentist))).all()
        
        if len(dentist_available_query) == 0:
            return True
        else:
            return False

class ReservationFormCancelButton(FlaskForm):
    cancel_button = SubmitField('Cancel')
