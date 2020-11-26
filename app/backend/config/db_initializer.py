from api.utlils import get_date_from_string
from config.db_handler import db
from model.dao import PatientDao, PatientTypeDao
from model.enums import PatientType, SexType


def set_default_pattients():
    patient_types = [
        PatientTypeDao(PatientType.NP, 'Normal Patient'),
        PatientTypeDao(PatientType.ZP, 'Patient bitten by Zombie')
    ]
    patients = [
        PatientDao('chuck_n@domain.com', 'Huck', 'Norris',
                   get_date_from_string('2020-03-23'), SexType.M, PatientType.NP),
        PatientDao('jt@test.ort', 'Jorh', 'Travolta',
                   get_date_from_string('2020-05-02'), SexType.M, PatientType.NP),
        PatientDao('marta.s@marta.com', 'Martha', 'Stewart',
                   get_date_from_string('2020-11-23'), SexType.F, PatientType.NP),
        PatientDao('denzel@aaa.com', 'Denzel', 'Washington',
                   get_date_from_string('2020-07-22'), SexType.M, PatientType.NP),
        PatientDao('jr@com.rb', 'John', 'Rambo',
                   get_date_from_string('2020-06-3'), SexType.M, PatientType.NP),
        PatientDao('jacky_C@bb.wb', 'Jacky', 'Chan',
                   get_date_from_string('2020-12-24'), SexType.M, PatientType.NP),
        PatientDao('susy_aaa@bb.com', 'Susan', 'Sarrandon',
                   get_date_from_string('2020-09-21'), SexType.F, PatientType.NP),
        PatientDao('reggym@com.aa', 'Magy', 'Reggy',
                   get_date_from_string('2020-11-22'), SexType.F, PatientType.NP),
        PatientDao('risck@walking.dd', 'Rick', 'Grimes',
                   get_date_from_string('2020-04-19'), SexType.M, PatientType.ZP),
        PatientDao('lc@bb.aa', 'Lili', 'Chilly',
                   get_date_from_string('2020-05-03'), SexType.F, PatientType.NP),
        PatientDao('rbalb@com.com', 'Rocly', 'Balboa',
                   get_date_from_string('2020-08-02'), SexType.M, PatientType.NP),
        PatientDao('Ppop@ppop.com', 'Prince', 'OfPersia',
                   get_date_from_string('2020-04-11'), SexType.M, PatientType.NP),
        PatientDao('lucky@luck.com', 'Lucky', 'Luck',
                   get_date_from_string('2020-02-22'), SexType.M, PatientType.NP),
        PatientDao('car_co@connor.com', 'Sarrah', 'Connor',
                   get_date_from_string('2020-03-19'), SexType.F, PatientType.NP),
        PatientDao('rrick@ri.com', 'Ricky', 'Rick',
                   get_date_from_string('2020-11-01'), SexType.M, PatientType.NP),
        PatientDao('pepa@com.com', 'Piter', 'Parker',
                   get_date_from_string('2020-05-03'), SexType.M, PatientType.NP)
    ]
    db.session.add_all(patient_types)
    db.session.add_all(patients)
    db.session.commit()
    db.session.close()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()
        set_default_pattients()
