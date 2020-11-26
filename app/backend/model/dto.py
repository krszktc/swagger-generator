from typing import List

from pydantic.main import BaseModel

from resources.generated_models import Pagination, Patient


class PatientResponse(BaseModel):
    data: List[Patient]
    links: Pagination


class PatientSaveData(BaseModel):
    birthdate: str
    email: str
    first_name: str
    last_name: str
    sex: str


class PatientSaveRequest(BaseModel):
    data: PatientSaveData
