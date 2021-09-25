from project.models import Patient
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired
from wtforms import ValidationError
from project.models import Patient


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class PatientRegistrationForm(FlaskForm):
    patient_email = StringField('Email', validators=[InputRequired(), Email()])
    patient_name = StringField('Name', validators=[DataRequired()])
    patient_surname = StringField('Surname', validators=[DataRequired()])
    patient_phone = StringField('Phone', validators=[InputRequired()])
    patient_password = PasswordField('Password', validators=[InputRequired(), EqualTo('patient_password_confirm', message="Passwords must match")])
    patient_password_confirm = PasswordField('Password_Confirm')
    submit = SubmitField('Register')

    def isNotExistEmail(self, data) -> bool:
        if Patient.query.filter_by(patient_email=data).first():
            return False
        else:
            return True

