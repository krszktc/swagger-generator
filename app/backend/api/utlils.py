from datetime import datetime
from typing import Dict, List

from model.dao import PatientDao
from model.enums import PatientType
from resources.generated_models import Attributes, Links, Patient

DEFAULT_PAGE_NUMBE = 1
DEFAULT_PAGE_SIZE = 1000
PAGE_NUMBER_PARAM = 'page'
PAGE_SIZE_PARAM = 'size'
DATE_FORMAT = '%Y-%m-%d'
DEFAULT_PATIENT_TYPE = PatientType.NP


ParamDict = Dict[str, List[str]]


def get_base_url(url: str) -> str:
    return url.split('?')[0]


def increase_param_number(param: List[str]) -> str:
    page_number = int(param[0]) + 1
    return str(page_number)


def get_date_from_string(date: str):
    return datetime.strptime(date, DATE_FORMAT).date()


def get_page_number(params: ParamDict) -> int:
    return int(params[PAGE_NUMBER_PARAM][0]) if PAGE_NUMBER_PARAM in params else DEFAULT_PAGE_NUMBE


def get_page_size(params: ParamDict) -> int:
    return int(params[PAGE_SIZE_PARAM][0]) if PAGE_SIZE_PARAM in params else DEFAULT_PAGE_SIZE


def get_next_url(params: ParamDict, current_url: str) -> str:
    params_url = ''
    separator = ','
    if PAGE_SIZE_PARAM in params:
        for key, value in params.items():
            if key == PAGE_NUMBER_PARAM:
                params_url = f'{params_url}&{key}={increase_param_number(value)}'
            else:
                params_url = f'{params_url}&{key}={separator.join(value)}'
        return f'{get_base_url(current_url)}?{params_url[1:]}'

    return current_url


def get_patient_dao_from_dto(dao: PatientDao, link: str, should_add_id: bool = False) -> Patient:
    self_url = f'{get_base_url(link)}/{dao.id}' if should_add_id else link
    links = Links(
        self=self_url
    )
    return Patient(
        attributes=Attributes(**dao.toParamsDict()),
        links=links,
        type=dao.patient_type_symbol
    )
