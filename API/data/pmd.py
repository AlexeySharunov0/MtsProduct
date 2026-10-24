from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Optional, Union, Any
from uuid import UUID

from pydantic import constr, Field, field_validator, HttpUrl, EmailStr, validator

from API.data.config_class import BaseModel


class DefaultResponse(BaseModel):
    code: int | str
    message: str
    details: List[Dict[str, str]]


###############################################  Ролевка


class AttributeInRole(BaseModel):
    code: str
    isEditable: bool
    isOwnedEditable: bool
    isOwnedView: bool
    isView: bool
    isEditingWithoutModeration: bool


class RoleCreation(BaseModel):
    id: str


class UserForRoles(BaseModel):
    login: str
    fullname: str
    avatar: str


class AllUsersModels(BaseModel):
    users: List[UserForRoles]


class RoleInLogin(BaseModel):
    roleName: str
    attributes: List[AttributeInRole]


class RolesByLogin(BaseModel):
    roles: List[RoleInLogin]


class Role(BaseModel):
    id: str
    name: str
    isActive: bool
    hasUser: bool
    hasAttribute: bool
    canDelete: bool


class RoleGroupInfo(BaseModel):
    type: str
    name: str
    items: list[Role]


class RoleGroup(BaseModel):
    role_group: list[RoleGroupInfo]


class AttributeInRoleById(BaseModel):
    id: str
    name: str
    isView: bool
    isEditable: bool
    isOwnedView: bool
    isOwnedEditable: bool
    isEditingWithoutModeration: bool


class RoleById(BaseModel):
    id: str
    name: str
    isActive: bool
    hasAttribute: bool
    type: str
    hasUser: bool
    attributes: List[AttributeInRoleById]
    users: List
    canDelete: bool


###############################################  Хранилище


class Specification(BaseModel):
    id: str
    name: str
    code: str


class Specifications(BaseModel):
    items: List[Specification]


class SpecificationCreation(BaseModel):
    id: str


class Value(BaseModel):
    id: str
    value: str
    code: str
    isActive: bool


class SpecificationLinkItem(BaseModel):
    id: str
    name: str
    required: bool


class AttributeForSpecificationById(BaseModel):
    id: str
    code: str
    name: str
    description: str
    isActive: bool
    type: str
    maxCount: int
    minCount: int
    values: List[Value]
    group: Any
    canDelete: bool
    createdAt: str
    specificationLink: List[SpecificationLinkItem]
    isMultiple: bool
    isRequired: bool


class SpecificationById(BaseModel):
    id: str
    name: str
    code: str
    attributes: List[AttributeForSpecificationById]


class SourceItem(BaseModel):
    id: str
    name: str
    link: str


class UsageType(BaseModel):
    id: str
    name: str


class Attribute(BaseModel):
    id: str
    code: str
    name: str
    description: str
    isActive: bool
    type: str
    maxCount: int
    minCount: int
    values: List[Value]
    group: Any
    canDelete: bool
    createdAt: str
    specificationLink: List[SpecificationLinkItem]
    isMultiple: bool
    source: Optional[SourceItem]
    usageType: UsageType


class Attributes(BaseModel):
    attributes: List[Attribute]


class AttributeCreation(BaseModel):
    id: str


class Sources(BaseModel):
    sources: List[SourceItem]


class SourceCreation(BaseModel):
    id: str


class DependedValue(BaseModel):
    code: str
    value: str


class DependetAttribute(BaseModel):
    code: str
    name: str
    values: list[DependedValue]


class AttributeById(BaseModel):
    id: str
    code: str
    name: str
    description: str
    isActive: bool
    type: str
    maxCount: int
    minCount: int
    values: List[Value]
    group: Any
    canDelete: bool
    createdAt: str
    specificationLink: List[SpecificationLinkItem]
    isMultiple: bool
    sourceId: str
    usageType: UsageType
    formula: str
    reasonForDeletion: str
    dependsOnAttribute: DependetAttribute | None


###############################################   Новости


class New(BaseModel):
    id: str
    name: str
    description: str
    isActive: bool
    imageLink: str
    createdAt: str
    weight: int


class News(BaseModel):
    news: List[New]


###############################################   Публичные спецификации

class PublicSpecification(BaseModel):
    id: str
    name: str
    code: str


class PublicSpecifications(BaseModel):
    items: List[PublicSpecification]


class PublicAttribute(BaseModel):
    id: str
    code: str
    name: str
    description: str
    isActive: bool
    type: str
    maxCount: int
    minCount: int
    values: List
    isMultiple: bool


class PublicAttributes(BaseModel):
    attributes: List[PublicAttribute]


class PublicValue(BaseModel):
    id: str
    value: str
    code: str
    isActive: bool


class PublicAttributeByCode(BaseModel):
    id: str
    code: str
    name: str
    description: str
    isActive: bool
    isRequired: bool
    type: str
    maxCount: int
    minCount: int
    isMultiple: bool
    usageType: str
    values: List[Value]
    reasonForDeletion: str


class PublicAttributesByCode(BaseModel):
    id: str
    name: str
    code: str
    attributes: List[PublicAttributeByCode]


###############################################   Интернал спецификации

class InternalValue(BaseModel):
    value: str
    code: str


class InternalAttribute(BaseModel):
    id: str
    name: str
    description: str
    isRequired: bool
    type: str
    isMultiple: bool
    isEditable: bool
    isEditingWithoutModeration: bool
    usageType: str
    values: List[InternalValue]


class InternalAttributes(BaseModel):
    attributes: List[InternalAttribute]


###############################################   Паблик Продукт в1

class DeletedProduct(BaseModel):
    code: str
    deletedAt: str


class DeletedProducts(BaseModel):
    products: List[DeletedProduct]


class Status(BaseModel):
    value: str
    code: str
    createdAt: str


class Product(BaseModel):
    code: str
    name: str
    type: str
    status: Status


class Products(BaseModel):
    products: List[Product]


class SourceItemProductByCode(BaseModel):
    name: str
    link: str


class ValueProductByCode(BaseModel):
    value: str
    code: str
    createdAt: str | Any


class AttributeProductByCode(BaseModel):
    code: str
    name: str
    editable: bool
    required: bool
    type: str
    maxCount: int
    minCount: int
    source: Union[str, SourceItemProductByCode] | None
    usageType: str
    values: List[ValueProductByCode]
    updatedAt: str
    isEditingWithoutModeration: bool
    reasonForDeletion: str


class LinkAttachment(BaseModel):
    link: str
    width: int
    height: int


class Attachment(BaseModel):
    id: str
    createAt: str
    type: str
    name: str
    description: str
    accessType: str
    links: List[LinkAttachment]


class ProductByCode(BaseModel):
    code: str
    name: str
    type: str
    description: str
    createdAt: str
    version: str
    attachments: List[Attachment]
    attributes: List[AttributeProductByCode]


class LinkInDocuments(BaseModel):
    link: str
    width: int
    height: int


class Document1InDocuments(BaseModel):
    id: str
    createAt: str
    type: str
    name: str
    description: str
    accessType: str
    links: List[LinkInDocuments]


class DocumentInDocuments(BaseModel):
    codeProduct: str
    NameProduct: str
    documents: List[Document1InDocuments]


class Documents(BaseModel):
    documents: List[DocumentInDocuments]


class ValueInSearch(BaseModel):
    value: str
    code: str
    createdAt: str | None


class LogoInSearch(BaseModel):
    link: str
    width: int
    height: int


class AttributeInSearch(BaseModel):
    code: str
    name: str
    editable: bool
    required: bool
    type: str
    maxCount: int
    minCount: int
    source: Union[str, SourceItemProductByCode] | None
    usageType: str
    values: List[ValueInSearch]
    updatedAt: str | None
    isEditingWithoutModeration: bool
    reasonForDeletion: str


class ProductInSearch(BaseModel):
    code: str
    name: str
    type: str
    description: str
    createdAt: str | None
    version: str
    attributes: List[AttributeInSearch]
    logos: List[LogoInSearch]


class SearchPublicProduct(BaseModel):
    products: List[ProductInSearch]


###############################################   Паблик Продукт в2


class AttributeProductV2(BaseModel):
    name: str
    code: str
    editable: bool
    required: bool
    type: str
    maxCount: int
    minCount: int
    values: List[ValueProductByCode]


class Logo(BaseModel):
    link: str
    width: int
    height: int


class ProductV2(BaseModel):
    code: str
    name: str
    description: str
    type: str
    createdAt: str
    version: str
    attributes: List[AttributeProductV2]
    logos: List[Logo]


class ProductsV2(BaseModel):
    products: List[ProductV2]


class AttributeUpdate(BaseModel):
    code: str
    name: str
    type: str
    updatedAt: str
    values: List[str]


class ProductUpdate(BaseModel):
    code: str
    name: str
    type: str
    attributes: List[AttributeUpdate]


class Update(BaseModel):
    products: List[ProductUpdate]


class ValueProductByCodeV2(BaseModel):
    value: str
    valueSpecId: str
    specValue: str
    specValueCode: str


class AttributeProductByCodeV2(BaseModel):
    id: str
    name: str
    code: str
    values: List[ValueProductByCodeV2]


class ProductByCodeV2(BaseModel):
    id: str
    code: str
    type: str
    name: str
    description: str
    version: str
    attributes: List[AttributeProductByCodeV2]


class ProductsByCode(BaseModel):
    products: List[ProductByCodeV2]


class ValueFavorite(BaseModel):
    value: str
    code: str
    createdAt: str
    additionalFields: Dict[str, Any]


class AttributeFavorite(BaseModel):
    name: str
    code: str
    editable: bool
    required: bool
    type: str
    maxCount: int
    minCount: int
    values: List[ValueFavorite]


class ProductFavorite(BaseModel):
    code: str
    name: str
    description: str
    type: str
    createdAt: str
    version: str
    attributes: List[AttributeFavorite]
    logos: List


class Favorites(BaseModel):
    products: List[ProductFavorite]


class ProductInSearchV2(BaseModel):
    code: str
    name: str


class SearchResult(BaseModel):
    products: List[ProductInSearchV2]


class ValueInAttrubutes(BaseModel):
    code: str
    value: str


class AttributeStory(BaseModel):
    code: str
    name: str
    type: str
    value: list[ValueInAttrubutes]


class ProductStory(BaseModel):
    code: str
    name: str
    type: str
    attributes: List[AttributeStory]


class Story(BaseModel):
    products: List[ProductStory]


###############################################   Рест экстернал

class ValueExternal(BaseModel):
    value: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    login: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None


class AttributeExternal(BaseModel):
    code: str
    name: str
    type: str
    values: List[ValueExternal]
    updatedAt: str


class ProductExternal(BaseModel):
    code: str
    name: str
    type: str
    description: str
    updatedAt: str
    attributes: List[AttributeExternal]


class ValueInAttributeListExternal(BaseModel):
    code: str
    name: str


class AttributeListExternal(BaseModel):
    attributes: List[ValueInAttributeListExternal]


class ProductsExternal(BaseModel):
    products: List[ProductExternal]


class ValueAttributesExternal(BaseModel):
    code: str
    value: str


class AttributeExternalRest(BaseModel):
    code: str
    name: str
    type: str
    description: str
    values: List[Any]


class AttributesExternalRest(BaseModel):
    attributes: List[AttributeExternalRest]


class PreviousStatusIntegration(BaseModel):
    statusCode: str
    statusName: str
    firstDate: Optional[str]
    secondDate: Any


class ReceivedStatuIntegration(BaseModel):
    statusCode: str
    statusName: str
    firstDate: str
    secondDate: Optional[str]


class Integration(BaseModel):
    id: str
    processedAt: Optional[str]
    date: str
    productCode: str
    productName: str
    previousStatus: PreviousStatusIntegration | None
    receivedStatus: Optional[ReceivedStatuIntegration]


class Integrations(BaseModel):
    integrations: List[Integration]


class OwnerRMS(BaseModel):
    login: str
    fullName: str


class ProjectRMS(BaseModel):
    code: int
    costCenter: str
    end: constr(min_length=1)
    expenseType: constr(min_length=1)
    name: constr(min_length=1)
    owner: OwnerRMS
    start: constr(min_length=1)
    status: constr(min_length=1)

    @field_validator('expenseType')
    def check_expense_type(cls, value):
        if value not in (expected_values := ('капекс', 'опекс', 'Non-utilization', '-')):
            raise AssertionError(f'Значения {value!r} нет среди ожидаемых {expected_values}')
        return value


class RMS(BaseModel):
    rms: List[ProjectRMS]


########## EDT

class ProductOwnerItemEDT(BaseModel):
    login: str
    fullName: str
    isFired: bool
    absenceType: str | None
    endAbsenceDate: str


class StatusCapability(BaseModel):
    code: str
    value: str


class ProductInEDT(BaseModel):
    code: str
    name: str
    type: str
    status: StatusCapability


class CapabilityItemEDT(BaseModel):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    number: str = Field(min_length=2)
    productOwner: Optional[ProductOwnerItemEDT]
    products: List[ProductInEDT]
    number: str


class ProductOwnerEDT(BaseModel):
    login: str
    fullName: str
    isFired: bool
    absenceType: str | None
    endAbsenceDate: str


class CapabilityEDT(BaseModel):
    code: str
    name: str


class ServedServiceEDT(BaseModel):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    status: str = Field(min_length=2)
    description: str
    productOwner: ProductOwnerEDT | None
    capability: CapabilityEDT
    criticalClass: str
    serviceType: str


class ProductOwner1EDT(BaseModel):
    login: str
    fullName: str
    isFired: bool
    absenceType: str | None
    endAbsenceDate: str


class CapabilityItem1EDT(BaseModel):
    code: str
    name: str


class RealizesServiceEDT(BaseModel):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    status: str = Field(min_length=2)
    description: str
    productOwner: Optional[ProductOwner1EDT]
    capability: Optional[CapabilityItem1EDT]
    criticalClass: str
    serviceType: str


class EDT(BaseModel):
    capability: List[CapabilityItemEDT]
    servedServices: List[ServedServiceEDT]
    realizesServices: List[RealizesServiceEDT]
    link: HttpUrl


#### Жизненый цикл

class ValueInLifeCycle(BaseModel):
    code: str
    name: str


class SpecificationInLifeCycle(BaseModel):
    editable: bool
    editableWithoutModeration: bool
    attributeCode: str
    AttributeName: str
    values: List[ValueInLifeCycle]


class AdditionalStatusInLifeCycle(BaseModel):
    code: str
    name: str
    startDate: str
    endDate: str
    documents: List


class DocumentInLifeCycle(BaseModel):
    name: str
    link: str
    extension: str
    type: str


class LinkInLifeCycle(BaseModel):
    name: str
    link: str
    extension: str
    type: str

class PlmItem(BaseModel):
    code: str
    name: str
    links: List[LinkInLifeCycle]


class StatusInLifeCycle(BaseModel):
    code: str
    name: str
    startDate: str
    endDate: str
    isActive: bool
    additionalStatuses: List[AdditionalStatusInLifeCycle]
    documents: List[DocumentInLifeCycle]
    plm: Optional[PlmItem]


class LifeCycle(BaseModel):
    specification: SpecificationInLifeCycle
    endFinancing: str
    statuses: List[StatusInLifeCycle]


##


class MatchingValue(BaseModel):
    code: str
    name: str


class OracleValidate(BaseModel):
    error: str
    matchingValues: List[MatchingValue]


class IndividualValue(BaseModel):
    value: str
    code: str


class IndividualAttribute(BaseModel):
    code: str
    name: str
    description: str
    type: str
    isMultiple: bool
    editingWithoutModeration: bool
    required: bool
    values: List[IndividualValue]


class IndividualSpecification(BaseModel):
    attributes: List[IndividualAttribute]


###############################################   Избранное


class NapravlenieGruppyInFavorites(BaseModel):
    code: str
    value: str


class PPinfoStatusInFavorites(BaseModel):
    code: str
    value: str


class RDInFavorites(BaseModel):
    code: str
    value: str


class TipObieektaUchetaInFavorites(BaseModel):
    code: str
    value: str


class PropertiesInFavorites(BaseModel):
    Napravlenie_gruppy: NapravlenieGruppyInFavorites
    PPinfo_status: PPinfoStatusInFavorites
    R_D: RDInFavorites = Field(..., alias='R&D')
    SYSTEM_ProductType: str
    Tip_obieekta_ucheta: TipObieektaUchetaInFavorites
    employee_product_owner: Optional[str] = None
    isBrand: Optional[bool] = None
    isInitClose: Optional[bool] = None
    isArchive: Optional[bool] = None
    isDeleted: Optional[bool] = None
    isEcosystemProduct: Optional[bool] = None
    PPInfo_main_product: Optional[str] = None


class FavoriteslItem(BaseModel):
    code: str
    name: str
    properties: PropertiesInFavorites


class FavoriteList(BaseModel):
    favorites: List[FavoriteslItem]


###############################################   Шаг в Product Guide

class LinkInProductGuide(BaseModel):
    name: str
    url: str


class ActionButtonsInProductGuide(BaseModel):
    name: str
    url: str


class EmployeeInProductGuide(BaseModel):
    avatar: str
    fullName: str
    isFired: bool
    login: str
    email: Optional[str] = None

    @field_validator('email')
    def validate_email(cls, value):
        if value in ('None', ''):
            return None
        elif '@' not in value or '.' not in value:
            raise ValueError('Invalid email address')
        return value


class FileInProductGuide(BaseModel):
    id: str
    link: str
    name: str
    size: int


class ValueItem(BaseModel):
    code: str
    value: str
    isEnable: bool


class FilterItem(BaseModel):
    codeAttribute: str
    nameAttribute: str
    value: List[ValueItem]


class GroupItem(BaseModel):
    id: str
    isEnable: bool
    name: str


class SubActionProductGuide(BaseModel):
    id: str
    isActive: bool
    for_po: bool
    for_cto: bool
    name: str
    required: bool
    repeatable: bool
    updatedAt: str
    weight: int
    duration: int
    schemeLink: str
    tags: list[str] | None


class ProductGuide(BaseModel):
    id: str
    name: str
    description: str
    isActive: bool
    createdAt: str
    updatedAt: str
    required: bool
    repeatable: bool
    for_po: bool
    for_cto: bool
    duration: int
    schemeLink: str
    tags: list | None
    groups: List[GroupItem]
    actionButtons: List[ActionButtonsInProductGuide]
    employees: List[EmployeeInProductGuide]
    files: List[FileInProductGuide]
    links: List[LinkInProductGuide]
    filter: List[FilterItem]
    subActions: List[SubActionProductGuide]


class SubActionFull(BaseModel):
    name: str
    description: str
    id: str
    required: bool
    repeatable: bool
    for_po: bool
    for_cto: bool
    duration: int
    schemeLink: str
    tags: list[str] | None
    actionButtons: List[ActionButtonsInProductGuide]
    links: List[LinkInProductGuide]
    files: List[FileInProductGuide]
    employees: List[EmployeeInProductGuide]


class Action(BaseModel):
    name: str
    description: str
    id: str
    required: bool
    repeatable: bool
    for_po: bool
    for_cto: bool
    duration: int
    schemeLink: str
    tags: list[str] | None
    actionButtons: List[ActionButtonsInProductGuide]
    links: List[LinkInProductGuide]
    files: List[FileInProductGuide]
    employees: List[EmployeeInProductGuide]
    subActions: List[SubActionFull]


class ActionInProduct(BaseModel):
    groupName: str
    id: str
    actions: List[Action]


class ActionsInProduct(BaseModel):
    actions: List[ActionInProduct]
    updatedAt: str


class ActionsInGeneral(BaseModel):
    actions_list: List[ActionInProduct]


###############################################   Список активных продукт гайдов

class ActiveProductGuideInList(BaseModel):
    name: str
    description: str
    createdAt: str
    updatedAt: str
    links: List[LinkInProductGuide]
    employees: List[EmployeeInProductGuide]
    files: List[FileInProductGuide]


class ListActiveProductGuide(BaseModel):
    guides: List[ActiveProductGuideInList]


###############################################   Список продукт гайдов
class ActionItem(BaseModel):
    id: str
    isActive: bool
    name: str
    typeProduct: str
    updatedAt: str
    weight: int
    for_po: bool
    for_cto: bool
    duration: int
    schemeLink: str
    tags: list[str] | None
    hasSubAction: bool


class ProductGuideInList(BaseModel):
    actions: List[ActionItem]
    groupName: str
    id: str


class ListProductGuide(BaseModel):
    guides: List[ProductGuideInList]


###### КУРАТОРЫ
class CuratorPerson(BaseModel):
    avatar: str
    fio: str
    isFired: bool
    login: str


class Curator(BaseModel):
    curators: List[CuratorPerson]
    isActive: bool
    name: str
    valueID: str


class CuratorsModel(BaseModel):
    curator_list: List[Curator]


class CuratorAttribute(BaseModel):
    id: str
    isMultiple: bool
    name: str


class CuratorAttributes(BaseModel):
    attributes: List[CuratorAttribute]


###### ДЕМО
# Модель для элементов в списке `files`
class File(BaseModel):
    id: str
    link: str
    name: str
    size: int  # Это согласно вашему примеру, если size всегда целое число


# Модель для элементов в списке `linkedProducts`
class LinkedProduct(BaseModel):
    productCode: str
    productName: str


class Category(BaseModel):
    id: UUID
    name: str


# Основная модель

class CategoryDemo(BaseModel):
    id: str
    name: str


class Demo(BaseModel):
    id: str
    name: str
    description: str
    link: str
    category: CategoryDemo
    conductedAt: str
    linkedProducts: List
    files: List


class Demos(BaseModel):
    demos: List[Demo]
    updatedAt: datetime


class Quarter(BaseModel):
    quarter: str
    demos: List[Demo]


class Quarters(BaseModel):
    quarters: List[Quarter]


class DemoInProduct(BaseModel):
    id: str
    name: str
    description: str
    link: str
    createdAt: str
    updatedAt: datetime


# Основная модель
class DemosInProduct(BaseModel):
    updatedAt: datetime
    links: List[DemoInProduct]


# Категории демо

class DemoCategory(BaseModel):
    id: UUID
    name: str
    description: str
    isActive: bool
    color: str


class DemosCategories(BaseModel):
    categories: List[DemoCategory]


# Результаты поиска демо

class DemoInSearch(BaseModel):
    id: str
    name: str
    categoryID: str
    categoryName: str
    conductedAt: datetime


class DemosInSearch(BaseModel):
    demos: List[DemoInSearch]


###### ИСТОРИЧНОСТЬ

class InitiatorItem(BaseModel):
    login: str
    fullName: str


class ModeratorItem(BaseModel):
    login: str
    fullName: str


class StoryUI(BaseModel):
    id: str
    date: str
    initiator: Optional[InitiatorItem]
    moderator: Optional[ModeratorItem]
    name: str
    type: str
    currentValues: List[str]
    previousValue: List[str]


class StoryForUI(BaseModel):
    story: List[StoryUI]


### EXTERNAL ШАГИ ПГ


class LinkExternal(BaseModel):
    name: str
    url: str


class FileExternal(BaseModel):
    id: str
    name: str
    size: int


class Link1External(BaseModel):
    name: str
    url: str


class SubActionExternal(BaseModel):
    id: str
    number: str
    name: str
    description: str
    contacts: List[str]
    links: List[Link1External]
    files: List


class ActionExternal(BaseModel):
    id: str
    number: str
    name: str
    description: str
    contacts: List[str]
    links: List[LinkExternal]
    files: List[FileExternal]
    subActions: List[SubActionExternal]


class GroupExternal(BaseModel):
    id: str
    groupName: str
    actions: List[ActionExternal]


class PGExternal(BaseModel):
    groups: List[GroupExternal]


###############################################   Мои продукты

class ProductInOwned(BaseModel):
    code: str
    name: str
    properties: Any


class ProductOwnerItem(BaseModel):
    fullname: str
    login: str


class ExecuterItem(BaseModel):
    fullname: str
    login: str


class DelegationProduct(BaseModel):
    id: str
    product: ProductInOwned
    productOwner: Optional[ProductOwnerItem]
    executer: Optional[ExecuterItem]


class PPinfoStatus(BaseModel):
    code: str
    value: str


class RD(BaseModel):
    code: str
    value: str


class TipObieektaUcheta(BaseModel):
    code: str
    value: str


class NapravlenieGruppy(BaseModel):
    code: str
    value: str


class KategoriiaKhaba(BaseModel):
    code: str
    value: str


class Properties(BaseModel):
    Napravlenie_gruppy: Optional[NapravlenieGruppy] = None
    PPinfo_status: PPinfoStatus
    R_D: Optional[RD] = Field(None, alias='R&D')
    SYSTEM_ProductType: str
    Tip_obieekta_ucheta: Optional[TipObieektaUcheta] = None
    employee_product_owner: Optional[str] = None
    isArchive: Optional[bool] = None
    isInitClose: Optional[bool] = None
    PPInfo_main_product: Optional[str] = None
    isDeleted: Optional[bool] = None
    isEcosystemProduct: Optional[bool] = None
    isNew: Optional[bool] = None
    isBrand: Optional[bool] = None
    Kategoriia_khaba: Optional[KategoriiaKhaba] = None


class OwnedProduct(BaseModel):
    code: str
    name: str
    properties: Properties


class Owned(BaseModel):
    delegationProducts: list[DelegationProduct]
    ownedProducts: list[OwnedProduct]


###############################################  Здоровье


class Cell(BaseModel):
    name: str
    hint: str
    value: str
    valueHint: str
    color: str


class HealthItem(BaseModel):
    code: str
    name: str
    hint: str
    description: str
    link: str
    cells: List[Cell]
    invalid: bool


class Health(BaseModel):
    health: List[HealthItem]
