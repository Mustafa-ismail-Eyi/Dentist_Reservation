#from werkzeug.wrappers import request
from werkzeug.wrappers.request import PlainRequest
from project.models import Patient, Dentist
from flask import Blueprint, render_template, flash, redirect, url_for, request
from project import db
from flask_login import current_user, login_user, logout_user, login_required
from project.patients.forms import LoginForm, PatientRegistrationForm
from project import socketio
import re

patients = Blueprint('patients', __name__)

@patients.route('/')
def index():
    return render_template('base.html')

@patients.route('/about')
def about():
    return render_template('welcome_user.html')

@patients.route('/login', methods=['GET','POST'])
def login_patient():
    email_pattern = '.+@(dentist)\.com'
    form = LoginForm()
    if form.validate_on_submit():
        # if there is a doc then the query below returns the doc's class
        if bool(re.match(email_pattern, form.email.data)):
            #print("DENTIST MAILINI YAKALADI")
            dent = Dentist.query.filter_by(dentist_email = form.email.data).first()
            if dent is not None:
                if dent.check_password(form.password.data) and dent is not None:
                    login_user(dent)
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('dent.welcome')
                    return redirect(next)
            else:
                print("DENTIST MAILINI YAKALAYAMADI")
                flash('Wrong email or password', category='error')
                return render_template('login.html',form=form)
        else:
            #print("PATIENT MAIL ADRESINI YAKALADI")
            patient = Patient.query.filter_by(patient_email = form.email.data).first()
            if patient is not None:
                if patient.check_password(form.password.data) and patient is not None:                 
                    login_user(patient)
                    print("USER LOGGED IN")
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('core.welcome')
                    return redirect(next)  
            else:
                #print("Wrong email or password")
                flash("Wrong email or password", category='error')    
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


def return_max_dentistid() -> int:
    return int(db.engine.execute("""SELECT max(dentist_id::bigint) as dentist_id from dentists""").all()[0][0])

@patients.route('/register', methods=['GET', 'POST'])
def register_patient():
    form = PatientRegistrationForm()
    email_pattern = '.+@(dentist)\.com'
    if form.validate_on_submit():
        # form.check_meail returns false if there is already email the user inputs
        if  form.isNotExistEmail(form.patient_email.data):
            if bool(re.match(email_pattern, form.patient_email.data)):
                dentist = Dentist(email=form.patient_email.data,
                                password=form.patient_password.data,
                                phone=form.patient_phone.data,
                                dentist_name= str(form.patient_name.data) + ' ' +str(form.patient_surname.data),
                                dentist_id= str(return_max_dentistid() + 1) )
                db.session.add(dentist)
                db.session.commit()
                flash("Successfully logged in",category='success')
                return redirect(url_for('patients.index'))
            else:
                patient = Patient(
                    email=form.patient_email.data,
                    name = form.patient_name.data,
                    surname = form.patient_surname.data,
                    password = form.patient_password.data,
                    phone = form.patient_phone.data
                    )
                db.session.add(patient)
                db.session.commit()            
                flash("you are registered successfully!", category="success")
                return redirect(url_for('patients.index'))
    return render_template('PatientRegister.html', form = form)

@patients.route('/logout')
@login_required
@socketio.on('disconnect')
def logout_patient():
    logout_user()
    return redirect(url_for('patients.index'))
