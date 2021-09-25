select  p.patient_name,
		p.patient_surname,
		r.reservation_datetime,
		r.patient_note,
		r.dentist_note_and_perscription,
		p.patient_phone,
		r.reservation_id
FROM dentists d LEFT JOIN reservations r ON d.dentist_id = r.dentist_id JOIN patients p ON r.patient_id = p.patient_id
--WHERE d.dentist_id = '11111111111'
ORDER BY r.reservation_datetime DESC

select * from dentists
select * from patients
SELECT max(dentist_id::bigint) as dentist_id from dentists


