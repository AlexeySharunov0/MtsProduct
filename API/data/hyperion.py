from __future__ import annotations

from pydantic import Field
from enum import Enum

from datetime import datetime

from API.data.config_class import BaseModel

########################################################################################################################   Hyperion

class ProjectStatuses(str, Enum):
    CONFIRMED = 'Подтвержден'
    CLOSED = 'Закрыт'

class ProductOwner(BaseModel):
    id: str
    login: str
    fullName: str
    surname: str
    middleName: str
    company: str
    department: str
    mobilePhone: str
    phone: str
    email: str
    avatar: str
    presentPost: str
    isFired: bool
    isInternal: bool


class Hyperion(BaseModel):
    hyperionCode: str = Field(min_length=5)
    projectName: str = Field(min_length=1)
    oracleCode: str = Field(min_length=1)
    projectStatus: ProjectStatuses
    openDate: datetime | str
    closeDate: datetime | str
    projectSuperCode: str
    productOwner: ProductOwner | None


class ListHyperion(BaseModel):
    hyperion: list[Hyperion]
