from project.models import Patient
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class UpdateDentistNoteForm(FlaskForm):
    dentist_note = TextAreaField("Note",validators=[DataRequired()])
    confirm_button = SubmitField(label="Confirm")