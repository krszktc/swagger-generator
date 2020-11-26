from api.utlils import *
from model.dao import PatientDao
from model.enums import PatientType, SexType


def test_get_base_url():
    """Should trim url from params"""
    assert get_base_url(
        'http://mainlink?pramA=3&paramb=4') == 'http://mainlink'


def test_increase_param_number():
    """Should increase param number"""
    assert increase_param_number(['5', '6', '7']) == '6'


def test_get_page_number():
    """Should return number interpertation of page or default value"""
    assert get_page_number({'page': ['5']}) == 5
    assert get_page_number({'param': ['5']}) == 1


def test_templae():
    """Should return number interpertation of size or default value"""
    assert get_page_size({'size': ['5']}) == 5
    assert get_page_size({'param': ['5']}) == 1000


def test_get_date_from_string():
    """Should data representation of string"""
    # GIVEN
    date_string = '2020-09-22'
    # WHEN
    date = get_date_from_string(date_string)
    # THEN
    assert date_string == str(date)


def test_get_next_url():
    """Should increase page number in case of param exist"""
    # GIVEN
    page_params = {'page': ['3'], 'size': ['10'], 'param': ['someValue']}
    non_page_params = {'size': ['10'], 'param': ['someValue']}
    param_url = 'http://someurl?page=3&size=10&param=someValue'
    non_param_url = 'http://someurl'
    # WHEN
    # THEN
    assert get_next_url(
        page_params, param_url) == 'http://someurl?page=4&size=10&param=someValue'
    assert get_next_url(
        page_params, non_param_url) == 'http://someurl?page=4&size=10&param=someValue'
    assert get_next_url(
        non_page_params, param_url) == 'http://someurl?size=10&param=someValue'
    assert get_next_url(
        non_page_params, non_param_url) == 'http://someurl?size=10&param=someValue'


def test_get_patient_dao_from_dto():
    """Should return Patient from dao with proper link and type"""
    # GIVEN
    dao = PatientDao('some_email@dmain.com', 'Name',
                     'Surname', '2020-10-10', SexType.F, PatientType.NP)
    dao.id = 111
    id_url = 'http://someurl/111'
    url = 'http://someurl'
    date_format = '%Y-%m-%d'
    # WHEN
    patient_1 = get_patient_dao_from_dto(dao, id_url)
    patient_2 = get_patient_dao_from_dto(dao, url, True)
    # THEN
    assert patient_1.links.self == patient_2.links.self == 'http://someurl/111'
    assert patient_1.attributes.id == patient_2.attributes.id == 111
    assert patient_1.attributes.first_name == patient_2.attributes.first_name == 'Name'
    assert patient_1.attributes.last_name == patient_2.attributes.last_name == 'Surname'
    assert patient_1.attributes.sex == patient_2.attributes.sex == 'F'
    assert patient_1.type == patient_2.type == 'NP'
    assert patient_1.attributes.birthdate.strftime(date_format) ==  \
        patient_2.attributes.birthdate.strftime(date_format) == '2020-10-10'
