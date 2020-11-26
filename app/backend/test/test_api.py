import copy
import json
from api.utlils import get_date_from_string

import connexion
import pytest
from alchemy_mock.mocking import AlchemyMagicMock
from sqlalchemy.exc import IntegrityError

from config.db_handler import db
from config.error_handler import init_error_handler
from model.dao import PatientDao
from model.dto import PatientResponse
from model.enums import PatientType, SexType
from resources.generated_models import Error, HttpError, Patient


@pytest.fixture(scope="module")
def app():
    app = connexion.App(__name__, specification_dir='../resources/')
    app.add_api('swagger.yaml',
                resolver=connexion.resolver.RestyResolver('api'))
    init_error_handler(app.app)

    return app.app.test_client()


@pytest.fixture
def attributes():
    dao_1 = PatientDao('mock_user_1@mock.com', 'MockName1', 'MockSurname1',
                       get_date_from_string('2020-01-01'), SexType.F, PatientType.NP)
    dao_1.id = 1
    dao_2 = PatientDao('mock_user_2@mock.com', 'MockName2', 'MockSurname2',
                       get_date_from_string('2020-02-02'), SexType.M, PatientType.NP)
    dao_2.id = 2
    dao_3 = PatientDao('mock_user_3@mock.com', 'MockName3', 'MockSurname3',
                       get_date_from_string('2020-03-03'), SexType.F, PatientType.NP)
    dao_3.id = 3

    return [dao_1, dao_2, dao_3]


@pytest.fixture
def post_request():
    return {
        'head': {
            'Content-Type': 'application/json',
            'Accept': 'application/problem+json'
        },
        'body': {
            'data': {
                'birthdate': '2020-10-23',
                'email': 'mock_email@mock.com',
                'first_name': 'SomeFirstName',
                'last_name': 'SomeLastName',
                'sex': 'F'
            }
        },
    }


def test_get_all_patiens(app, attributes):
    """Should return colleciton of patients"""
    # GIVEN
    db.session = AlchemyMagicMock()
    db.session.query.return_value.order_by.return_value.paginate.return_value.items = attributes
    # WHEN
    response = app.get('/v1/patients')
    response_data = PatientResponse(**json.loads(response.data))
    # THEN

    assert response.status_code == 200
    assert len(response_data.data) == 3
    assert response_data.links.self == response_data.links.next == 'http://localhost/v1/patients'

    assert response_data.data[0].attributes.id == attributes[0].id
    assert response_data.data[0].attributes.first_name == attributes[0].name
    assert response_data.data[0].attributes.last_name == attributes[0].surname
    assert response_data.data[0].attributes.email == attributes[0].email
    assert response_data.data[0].attributes.sex == attributes[0].sex
    assert response_data.data[0].attributes.birthdate == attributes[0].birthdate
    assert response_data.data[0].links.self == 'http://localhost/v1/patients/1'
    assert response_data.data[0].type == 'NP'

    assert response_data.data[1].attributes.id == attributes[1].id
    assert response_data.data[1].attributes.first_name == attributes[1].name
    assert response_data.data[1].attributes.last_name == attributes[1].surname
    assert response_data.data[1].attributes.email == attributes[1].email
    assert response_data.data[1].attributes.sex == attributes[1].sex
    assert response_data.data[1].attributes.birthdate == attributes[1].birthdate
    assert response_data.data[1].links.self == 'http://localhost/v1/patients/2'
    assert response_data.data[1].type == 'NP'

    assert response_data.data[2].attributes.id == attributes[2].id
    assert response_data.data[2].attributes.first_name == attributes[2].name
    assert response_data.data[2].attributes.last_name == attributes[2].surname
    assert response_data.data[2].attributes.email == attributes[2].email
    assert response_data.data[2].attributes.sex == attributes[2].sex
    assert response_data.data[2].attributes.birthdate == attributes[2].birthdate
    assert response_data.data[2].links.self == 'http://localhost/v1/patients/3'
    assert response_data.data[2].type == 'NP'


def test_get_patient_by_id(app, attributes):
    """Should return patient by provided ID"""
    # BUG: SQLAlchemy first.return_value doesnt work!
    # When fixed, workaround can be remove and below assignmen used:
    # db.session.query.return_value.filter_by.return_value.first.return_value = attributes[1]
    # GIVEN
    db.session = AlchemyMagicMock()

    def workaround():
        return attributes[1]

    db.session.query.return_value.filter_by.return_value.first = workaround
    # WHEN
    response = app.get('/v1/patients/2345')
    response_data = Patient(**json.loads(response.data))
    # THEN
    assert response.status_code == 200

    assert response_data.attributes.id == attributes[1].id
    assert response_data.attributes.first_name == attributes[1].name
    assert response_data.attributes.last_name == attributes[1].surname
    assert response_data.attributes.email == attributes[1].email
    assert response_data.attributes.sex == attributes[1].sex
    assert response_data.attributes.birthdate == attributes[1].birthdate
    assert response_data.links.self == 'http://localhost/v1/patients/2345'
    assert response_data.type == 'NP'


def test_create_new_patient(app, post_request):
    """Should successfully save patient"""
    # GIVEN
    def set_dao_id(dao: PatientDao) -> PatientDao:
        dao.id = 15
        return PatientDao

    db.session = AlchemyMagicMock()
    db.session.add = set_dao_id
    # WHEN
    response = app.post('/v1/patients', 'http://mock_server_url',
                        headers=post_request['head'],
                        data=json.dumps(post_request['body']))
    response_data = Patient(**json.loads(response.data))
    # THEN
    assert response.status_code == 200

    request_data = post_request['body']['data']
    assert response_data.attributes.id == 15
    assert response_data.type == 'NP'
    assert response_data.attributes.first_name == request_data['first_name']
    assert response_data.attributes.last_name == request_data['last_name']
    assert response_data.attributes.email == request_data['email']
    assert response_data.attributes.sex == request_data['sex']
    assert response_data.links.self == 'http://mock_server_url/v1/patients/15'
    assert response_data.attributes.birthdate == \
        get_date_from_string(request_data['birthdate'])


def test_create_patient_wrong_param(app, post_request):
    """Should return error with info about missing field"""
    # GIVEN
    request_body = copy.deepcopy(post_request['body'])
    del request_body['data']['first_name']
    # WHEN
    response = app.post('/v1/patients', 'http://mock_server_url',
                        headers=post_request['head'],
                        data=json.dumps(request_body))

    # BUG: Swagger saying about HttpError model but sending different model in response
    response_data = Error(**json.loads(response.data))
    # THEN
    assert response.status_code == 400
    assert 'first_name', 'required' in response_data.detail


def test_create_patient_wront_sex_type(app, post_request):
    """Should rerurn error with info about wrong sex"""
    # GIVEN
    request_body = copy.deepcopy(post_request['body'])
    request_body['data']['sex'] = 'BOOOM!'
    # WHEN
    response = app.post('/v1/patients', 'http://mock_server_url',
                        headers=post_request['head'],
                        data=json.dumps(request_body))
    response_data = HttpError(**json.loads(response.data))
    # THEN
    assert response.status_code == 400
    assert response_data.error.detail == "Wront Sex type. Use 'F' or 'M'"


def test_create_patient_double_email(app, post_request):
    """Should rerurn error with info about email which already exist in db"""
    # GIVEN
    def broken_function(dao):
        raise IntegrityError('statement', 'params', 'orig')

    db.session = AlchemyMagicMock()
    db.session.add = broken_function
    # WHEN
    response = app.post('/v1/patients', 'http://mock_server_url',
                        headers=post_request['head'],
                        data=json.dumps(post_request['body']))
    response_data = HttpError(**json.loads(response.data))
    # THEN
    assert response.status_code == 409
    assert response_data.error.detail == 'Mail already exist'
