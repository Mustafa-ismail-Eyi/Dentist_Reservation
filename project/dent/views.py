from sqlalchemy.engine import url
from werkzeug.utils import validate_arguments
from project.models import Patient, Dentist, Reservations
from flask import Blueprint, render_template, flash, redirect, url_for, request
from project import db
from flask_login import current_user, logout_user, login_required
from project.dent.forms import UpdateDentistNoteForm

dent = Blueprint('dent',__name__)

@login_required
def checkDentistHasReservation():
    if Reservations.query.filter_by(dentist_id=current_user.dentist_id).first() is not None:
        return True
    else:
        return False


@dent.route('/')
@dent.route('/DocWelcome')
@login_required
def welcome():
    # burada kaldın
    checkDentistResevation = checkDentistHasReservation() 
    if checkDentistResevation:
        dentist_reservations = db.engine.execute("""
        select  p.patient_name,
        p.patient_surname,
        r.reservation_datetime,
        r.patient_note,
        r.dentist_note_and_perscription,
        p.patient_phone,
        r.reservation_id
        FROM dentists d LEFT JOIN reservations r ON d.dentist_id = r.dentist_id JOIN patients p ON r.patient_id = p.patient_id
        WHERE d.dentist_id = '{dentist_id}'
        ORDER BY r.reservation_datetime DESC""".format(dentist_id = current_user.dentist_id)).all()
        return render_template('dentIndex.html', dentistHasReservation = checkDentistResevation, dentist_reservations = dentist_reservations)
    else:
        return render_template('dentIndex.html')



@dent.route('/pre-update-reservation/<int:reservation_id>', methods=['GET','POST'])
def pre_update_reservation(reservation_id):
    form = UpdateDentistNoteForm()
    if form.validate_on_submit():
        dentist_note = form.dentist_note.data
        return redirect(url_for('reservations.update_reservation',reservation_id=int(reservation_id),dentist_note=dentist_note))
    return render_template("preUpdateReservation.html", form=form)

@dent.route('/DocLogout')
@login_required
def logout_dent():
    logout_user()
    return redirect(url_for('patients.index'))