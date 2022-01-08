from datetime import datetime,date
from flask_migrate import current
from project.patients.views import login_patient
from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_wtf import form
from flask_login import login_required, current_user
from project.core.forms import ReservationForm
from project.models import Reservations
from project import db
from project.models import Patient, Reservations, Dentist
from sqlalchemy import text, and_, cast, DATE


core = Blueprint('core', __name__)

@login_required
def checkUserHasReservation():
    if Reservations.query.filter(and_(cast(Reservations.reservation_datetime,DATE) >= date.today(), Reservations.patient_id==current_user.patient_id)).first() is not None:
        # cast(reservation_datetime,DATE) > date.today())filter_by(patient_id=current_user.patient_id)
        return True
    else:
        return False
        
@core.route('/welcome')
def welcome():
    checkCurrent_userReservation = checkUserHasReservation()
    reservation_info = None
    if checkCurrent_userReservation:
        #Reservations.query.join(Patient, Reservations.patient_id == Patient.patient_id).filter_by().order_by(Reservations.reservation_book_date.asc())
        reservation_info = db.engine.execute(text("""select p.patient_name as patient_name,
                                                            p.patient_surname as patient_surname, 
                                                            r.reservation_datetime as res_date, 
                                                            d.dentist_name_surname as dentist_name, 
                                                            r.patient_note,
                                                            r.dentist_note_and_perscription,
                                                            r.reservation_id
                                                    from patients p JOIN reservations r ON r.patient_id = p.patient_id 
	                                                JOIN dentists d ON r.dentist_id = d.dentist_id where p.patient_name='{name}' and p.patient_surname='{surname}'
                                                    ORDER BY res_date DESC""".format(name=current_user.patient_name, surname=current_user.patient_surname))).all()
        return render_template('index.html', reservationValidation = checkCurrent_userReservation, reservation_info = reservation_info)
                                            
    return render_template('index.html', reservationValidation = checkCurrent_userReservation, reservation_info=reservation_info)





@core.route('/select-date', methods=['GET','POST'])
def booking_patient():
    form = ReservationForm()
    #'YYYY-MM-DD HH:MM:SS' formatında 
    book_date = form.reservation_datetime.data
    # print(book_date, "heellloooo")

    if form.validate_on_submit():
        book_date = form.reservation_datetime.data
        doc_name = form.reservation_doctor_name.data
        patient_note = form.reservation_patient_note.data
        if form.isDateValid(book_date):
            if form.isTimeValid(book_date):
                if form.isDentistAvailable(book_date, doc_name):
                    flash("Congrats you successfully made a reservation")
                    reservation = Reservations(
                        patient_id = current_user.patient_id,
                        dentist_id= Dentist.query.filter_by(dentist_name_surname=doc_name).first().dentist_id,
                        date_time= book_date,
                        patient_note= patient_note,
                        dentist_notes= ""
                    )
                    db.session.add(reservation)
                    db.session.commit()
                    flash("Congrats you successfully made a reservation")
                    return redirect(url_for('core.welcome'))
                else:
                    flash("This hour of date is already reservated. Please pick another hour of date", category="warning")
                    return render_template("PatientBooking.html", form = form)
            else:
                flash("Invalid hour please pick an hour in workdays", category="warning")
                return render_template("PatientBooking.html", form = form)
            
        else:
            flash("Invalid Date", category="warning")
            return render_template("PatientBooking.html", form = form)
    return render_template("PatientBooking.html", form = form)
