from flask.helpers import url_for
from werkzeug.utils import redirect
from project import db
from flask import Blueprint
from flask import request
from flask_login import current_user, login_required

reservations = Blueprint('reservations', __name__)

@reservations.route('/delete/<int:reservation_id>', methods=['GET','POST'])
@login_required
def delete_reservation(reservation_id):
    if request.method == 'POST':
        if request.form.get('res_cancel') == 'Cancel':
            db.engine.execute("""DELETE FROM reservations r WHERE r.patient_id = {pid} AND r.reservation_id = {reservation_id}""".\
                format(pid=current_user.patient_id, reservation_id=reservation_id))
    return redirect(url_for('core.welcome'))


@login_required
@reservations.route('/update/<int:reservation_id>/<dentist_note>', methods=['GET','POST'])
def update_reservation(reservation_id, dentist_note):
#    if request.method == 'POST':
#        if request.form.get('res_update') == 'Update':
    db.engine.execute("""UPDATE reservations SET dentist_note_and_perscription = '{dentist_note_}' WHERE reservation_id = '{reservation_id}'""".\
        format(dentist_note_=dentist_note,reservation_id=reservation_id))
    return redirect(url_for('dent.welcome'))

