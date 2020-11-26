import math
from typing import Dict

import connexion

from api.utlils import *
from config.db_handler import db
from model.dao import PatientDao
from model.dto import PatientResponse, PatientSaveRequest
from model.enums import SexType
from resources.generated_models import Pagination, Patient


def search() -> PatientResponse:
    request_url = connexion.request.url
    request_params = connexion.request.args.to_dict(flat=False)
    results = db.session.query(PatientDao)  \
        .order_by(PatientDao.surname)       \
        .paginate(
            get_page_number(request_params),
            get_page_size(request_params)
    ).items
    db.session.close()

    return PatientResponse(
        data=list(
            map(lambda result: get_patient_dao_from_dto(
                result, request_url, True), results)
        ),
        links=Pagination(
            self=request_url,
            next=get_next_url(request_params, request_url)
        )
    ).dict()


def get(id: int) -> Patient:
    request_url = connexion.request.url
    result = db.session.query(PatientDao)   \
        .filter_by(id=id)                   \
        .first()
    db.session.close()

    return get_patient_dao_from_dto(result, request_url).dict()


def post(body: Dict) -> Patient:
    body_model = PatientSaveRequest(**body)
    request_url = connexion.request.url
    patient_to_save = PatientDao(
        body_model.data.email,
        body_model.data.first_name,
        body_model.data.last_name,
        get_date_from_string(body_model.data.birthdate),
        SexType[body_model.data.sex],
        DEFAULT_PATIENT_TYPE
    )
    db.session.add(patient_to_save)
    db.session.commit()
    db.session.flush()

    request_response = get_patient_dao_from_dto(
        patient_to_save, request_url, True).dict()
    db.session.close()

    return request_response
