from __future__ import annotations

from typing import List

from pydantic import Field, constr

from API.data.config_class import BaseModel


############################################ Список доп юзеров

class Employee(BaseModel):
    login: str
    firstName: str
    lastName: str
    middleName: str
    position: str
    mobilePhone: str
    internalPhone: str
    email: str
    department: str
    company: str
    pulseLink: str


class EmployeeList(BaseModel):
    employees: List[Employee]


############################################ Юзеры из результатов поиска

class User(BaseModel):
    id: str
    login: str = Field(..., description='Логин пользователя')
    fullName: constr(min_length=1, strict=True)
    company: str
    department: str
    mobilePhone: str
    phone: str
    email: str
    avatar: str
    presentPost: str
    compatibility: bool
    pulseLink: str

class Absence(BaseModel):
    absenceType: str
    date: str

class Product(BaseModel):
    code: str
    name: str
    roles: str


class UserLogin(BaseModel):
    id: str
    login: str = Field(..., description='Логин пользователя')
    fullName: constr(min_length=1, strict=True)
    company: str
    isFired: bool
    department: str
    mobilePhone: str
    phone: str
    email: str
    avatar: str
    presentPost: str
    compatibility: bool
    pulseLink: str
    absence: Absence | None
    products: list[Product]



class Users(BaseModel):
    users: List[User]


############################################ Юзеры из результатов другого поиска


class UserInSearch(BaseModel):
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
    compatibility: bool


class UsersInSearch(BaseModel):
    users: List[UserInSearch]


############################################ Запрос текущего юзера


class GetUser(BaseModel):
    fullName: str
    login: str
    avatar: str
    email: str
    groups: List[str]
    email: str
