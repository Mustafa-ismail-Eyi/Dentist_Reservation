ALTER TABLE dentists ADD COLUMN dentist_name_surname varchar(64)

SELECT * FROM dentists

UPDATE dentists set dentist_name_surname = 'Saruhan OYMACI' 
where dentist_email = 'saruhan@dentist.com'

UPDATE dentists set dentist_name_surname = 'Tuncer Besne'
where dentist_email = 'tuncer@dentist.com'

UPDATE dentists set dentist_name_surname = 'Kaan Çetin'
where dentist_email = 'kaan@dentist.com'

ALTER TABLE dentists ALTER COLUMN dentist_name_surname SET  NOT NULL