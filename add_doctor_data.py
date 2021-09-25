from project import db
from project.models import Dentist
from flask_sqlalchemy import SQLAlchemy

dentist_1 = Dentist("saruhan@dentist.com", "365478", "+905451111111", "11111111111")
dentist_2 = Dentist("tuncer@dentist.com", "365478", "+905451111112","11111111112")
dentist_3 = Dentist("kaan@dentist.com", "365478", "+905451111113", "11111111113")

db.session.add_all([dentist_1, dentist_2,dentist_3])
