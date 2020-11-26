from sqlalchemy.sql.expression import null
from model.enums import PatientType, SexType
from sqlalchemy import Integer, String, Date
from sqlalchemy.sql.schema import (
    Column, ForeignKey, ForeignKeyConstraint, Sequence)

from config.db_handler import db


class PatientTypeDao(db.Model):
    __tablename__ = 'patient_type'
    symbol = Column(String, primary_key=True)
    description = Column(String)

    def __init__(self, symbol: PatientType, description):
        self.symbol = symbol.name
        self.description = description


class PatientDao(db.Model):
    __tablename__ = 'patients'
    __table_args__ = (
        ForeignKeyConstraint(
            ['patient_type_symbol'],
            ['patient_type.symbol'],
            name="fk_patient_type_sybol"
        ),
    )

    id = Column(Integer, Sequence('patient_id_seq'), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    sex = Column(String, nullable=False)
    patient_type_symbol = Column(String, ForeignKey('patient_type.symbol'))

    def __init__(self, email: str, name: str, surname: str,
                 birthdate: Date, sex: SexType, patient_type: PatientTypeDao):
        self.email = email
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.sex = sex.name
        self.patient_type_symbol = patient_type.name

    def toParamsDict(self):
        return {
            'id': self.id,
            'first_name': self.name,
            'last_name': self.surname,
            'birthdate': self.birthdate,
            'email': self.email,
            'sex': self.sex,
            'type': self.patient_type_symbol
        }
