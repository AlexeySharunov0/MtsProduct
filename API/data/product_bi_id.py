from __future__ import annotations

from typing import List, Any, Optional

from API.data.config_class import BaseModel


###############################################   Информация о продукте по коду


class NameProduct(BaseModel):
    id: str
    value: str
    name: str
    description: str
    required: bool
    editable: bool


class DescriptionProduct(BaseModel):
    id: str
    value: str
    name: str
    description: str
    required: bool
    editable: bool


class Value(BaseModel):
    code: str
    value: str


class Answer(BaseModel):
    code: str
    value: str


class SourceItem(BaseModel):
    name: str
    link: str


class DependedValue(BaseModel):
    code: str
    value: str


class DependetAttribute(BaseModel):
    code: str
    name: str
    values: list[DependedValue]


class Header(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    dependentAttribute: DependetAttribute | None
    values: List[Value]
    answers: List[Answer]
    source: Optional[SourceItem]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str

class Absence(BaseModel):
    dateEndAbsence: str
    typeAbsence: str


class User(BaseModel):
    login: str
    fullName: str
    avatar: str
    isFired: bool
    email: str
    absence: Absence | None
    


class UserInProduct(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List[User]
    values: List[Value]
    answers: List
    source: Optional[SourceItem]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



class Link(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List[Value]
    answers: List
    source: Optional[SourceItem]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



##


class HidingAttribute(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List[User]
    values: List[Value]
    answers: List[Answer]
    source: Optional[SourceItem]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



##


class Attribute(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List[User]
    values: List[Value]
    answers: List[Answer]
    source: Optional[SourceItem]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



class GroupAttribute(BaseModel):
    id: str
    name: str
    attributes: List[Attribute]


class Value1(BaseModel):
    code: str
    value: str


class SourceItem1(BaseModel):
    name: str
    link: str


class DescriptionLink(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List[Value1]
    answers: List
    source: Optional[SourceItem1]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



class Value2(BaseModel):
    code: str
    value: str


class SourceItem2(BaseModel):
    name: str
    link: str


class ActionLink(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List[Value2]
    answers: List
    source: Optional[SourceItem2]
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None



class Type(BaseModel):
    code: str
    value: str


class SourceItem3(BaseModel):
    name: str
    link: str


class RatingItem(BaseModel):
    name: str
    delta: str
    mark: str
    source: Optional[SourceItem3]
    createdAt: str
    reasonForDeletion: str
    description: str


class Product(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List
    answers: List
    source: Any
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str


class Value3(BaseModel):
    code: str
    value: str


class MetricsLink(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List[Value3]
    answers: List
    source: Any
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str


class Status(BaseModel):
    code: str
    value: str


class Grade(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List
    answers: List
    source: Any
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: DependetAttribute | None

class ValueInCorner(BaseModel):
    code: str
    value: str


class AnswerInCorner(BaseModel):
    code: str
    value: str

class CornerChipAttribute(BaseModel):
    id: str
    name: str
    type: str
    required: bool
    editable: bool
    description: str
    users: List
    values: List[ValueInCorner]
    answers: List[AnswerInCorner]
    source: Any
    usageType: str
    isMultiple: bool
    updatedAt: str
    editingWithoutModeration: bool
    reasonForDeletion: str
    dependentAttribute: Any



class ProductBiId(BaseModel):
    id: str
    name: NameProduct
    RmsStaff: HidingAttribute
    description: DescriptionProduct
    headers: List[Header]
    users: List[UserInProduct]
    links: List[Link]
    cornerChipAttributes: list[CornerChipAttribute]
    canvas: List[HidingAttribute]
    hidingAttributes: List[HidingAttribute]
    groupAttributes: List[GroupAttribute]
    descriptionLinks: List[DescriptionLink]
    actionLinks: List[ActionLink]
    mainProduct: Any
    oracleId: Any
    type: Type
    rating: List[RatingItem]
    financing: List[HidingAttribute]
    editable: bool
    isEditFile: bool
    isEco: bool
    isNew: bool
    isHub: bool
    metricsLinks: List[MetricsLink]
    reasonDeletion: Any
    status: Status
    updatedAt: str
    technicalMaturity: List[Grade]
    isEditFileWithoutModeration: bool
    updatedAt: str
