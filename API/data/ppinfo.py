from __future__ import annotations

from typing import List, Any, Optional

from API.data.config_class import BaseModel


class Executors(BaseModel):
    login: str
    fullName: str
    avatarUrl: str


class Author(BaseModel):
    login: str
    fullName: str
    avatarUrl: str


class Comment(BaseModel):
    id: str
    user: str | None
    type: str
    comment: str


class Brief(BaseModel):
    id: str
    type: str
    status: str
    createAt: str
    doneDate: str
    productName: str
    number: str
    executors: Executors | None
    author: Author
    comments: List[Comment]


class StatusBrief(BaseModel):
    status: str
    name: str
    count: int


class StatusesBrief(BaseModel):
    statuses: List[StatusBrief]


class Briefs(BaseModel):
    briefs: List[Brief]


class AuthorBriefById(BaseModel):
    login: str
    fullName: str
    avatarUrl: str
    managersDelegatedRole: List

class ProductBrief(BaseModel):
    id: str
    name: str
    type: str

class Value(BaseModel):
    code: str
    value: str

class CurrentAttribute(BaseModel):
    id: str
    values: List[Value]

class BriefById(BaseModel):
    id: str
    type: str
    data: str
    status: str
    createAt: str
    number: str
    doneDate: str
    executor: Executors | Any
    draft: Any
    author: AuthorBriefById
    comments: List
    currentAttributes: List
    product: ProductBrief | None


class Draft(BaseModel):
    data: str
    createAt: str


class DraftInList(BaseModel):
    login: str
    createAt: str


class DraftsList(BaseModel):
    drafts: List[DraftInList]


class BriefDoc(BaseModel):
    id: str
    processId: str


###############################################   Метрики


class MetricLinks(BaseModel):
    name: str
    code: str
    description: str
    value: str


class Metric(BaseModel):
    metricsLinks: List[MetricLinks]
    typeText: int


############################################### Заявки пользователя


class Product(BaseModel):
    id: str
    name: str
    type: str


class UserItem(BaseModel):
    name: str
    avatar: str


class UBrief(BaseModel):
    id: str
    number: str
    status: str
    type: str
    createdAt: str
    moderationAt: str
    comment: str
    product: Product | None
    user: Optional[UserItem]


class UserBriefs(BaseModel):
    briefs: List[UBrief]

############################################### Документы в продукте по коду
class DocumentInProductByCode(BaseModel):
    id: str
    name: str
    link: str
    comment: str
    createdAt: str


class DocumentsInProductByCode(BaseModel):
    documents: List[DocumentInProductByCode]


class Attr(BaseModel):
    code: str
    name: str


class AttrList(BaseModel):
    attributes: List[Attr]


class DraftInUser(BaseModel):
    externalId: str
    data: str
    type: str
    createAt: str


class User(BaseModel):
    fullName: str
    firstName: str
    lastName: str
    login: str
    externalId: str
    email: str
    avatar: str
    groups: List[str]
    tutorials: List
    isTutoringCompleted: bool
    isFired: bool
    drafts: List[DraftInUser] | None
    isInternal: bool


###############################################   Юзер


class UserSSO(BaseModel):
    fullName: str
    firstName: str
    lastName: str
    login: str
    externalId: str
    email: str
    avatar: str
    groups: List[str]
    tutorials: List[str]
    isTutoringCompleted: bool
    isFired: bool
    drafts: List[DraftInUser]
    isInternal: bool


class UserByLogin(BaseModel):
    avatar: str
    company: str
    delegated: bool
    department: str
    email: str
    firstName: str
    fullName: str
    id: str
    login: str
    middleName: str
    mobilePhone: str
    phone: str
    presentPost: str
    surname: str
    isFired: bool


############################################### Уволенные сотрудники


class Position1(BaseModel):
    attributeId: str
    attributeName: str


class StatusFired(BaseModel):
    attributeId: str
    attributeName: str


######################################################################################################### Системы IMS и приложения SAM

class LinkInSystem(BaseModel):
    name: str
    url: str

class Application(BaseModel):
    name: str
    code: str
    link: str
    status: str


class PlannedItem(BaseModel):
    application: Application
    systems: List[System]


class System(BaseModel):
    id: str
    name: str
    statusName: str
    supportTeamName: str
    supportTeamId: str
    type: str
    criticalityClass: int


class WorkedItem(BaseModel):
    application: Application
    systems: List[System]


class InformationSystems(BaseModel):
    planned: List[PlannedItem]
    worked: List[WorkedItem]
    links: List[LinkInSystem]


############################################### Атрибуты в типах для фильтров

class ValueInFilter(BaseModel):
    code: str
    value: str


class AttributeForFilters(BaseModel):
    id: str
    name: str
    description: str
    type: str
    required: bool
    values: List[ValueInFilter]
    isMultiply: bool
    editingWithoutModeration: bool


class AttributesForFilters(BaseModel):
    attributes: List[AttributeForFilters]


############################################### Атомарные продукты

class StatusInAtomic(BaseModel):
    value: str
    code: str
    date: str


class User1InAtomic(BaseModel):
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


class UserInAtomic(BaseModel):
    weight: int
    type: str
    name: str
    users: List[User1InAtomic]


class ProductInAtomic(BaseModel):
    id: str
    description: str
    name: str
    status: StatusInAtomic
    ratings: List
    users: List[UserInAtomic]
    links: List
    attributes: List


class Atomics(BaseModel):
    products: List[ProductInAtomic]


######################################################################################################################## Davinci

class Owner(BaseModel): # Owner
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


class Project(BaseModel):
    link: str
    code: str
    name: str
    user: Optional[Owner]
    dateEnd: str
    dateStart: str
    status: str


class Davinci(BaseModel):
    projects: List[Project]


############################################### Юзеры в репорте


class ProductReport(BaseModel):
    id: str
    name: str
    startClose: bool
    status: StatusFired
    type: StatusFired


class PositionReport(BaseModel):
    position: Position1
    products: List[ProductReport]


class UserReport(BaseModel):
    login: str
    fullName: str
    positions: List[PositionReport]


class ReportItem(BaseModel):
    name: str
    count: int
    users: List[UserReport]


class Report(BaseModel):
    report: List[ReportItem]


##################################################### EPM / ECO-MODULES


class ProductStatus(BaseModel):
    code: str
    value: str


class Row(BaseModel):
    id: str
    description: str
    link: str


class Module(BaseModel):
    productId: str
    productName: str
    productStatus: ProductStatus
    rows: List[Row]


class Modules(BaseModel):
    headers: List[str]
    modules: List[Module]


###### EPM

class Product(BaseModel):
    productId: str
    productName: str
    productStatus: ProductStatus
    rows: List[Row]


class EcoModule(BaseModel):
    headers: List[str]
    products: List[Product]


#### TAG

class UserTag(BaseModel):
    login: str
    name: str
    type: str
    avatar: str
    email: str


class AttributeTag(BaseModel):
    id: str
    name: str
    isEnable: bool
    weight: int
    isDisable: bool


class TagClass(BaseModel):
    id: str
    name: str
    description: str
    type: str
    group: str
    hasWeight: bool
    hasAttributes: bool
    hasUsers: bool
    attributes: List[AttributeTag] | Any
    users: List[UserTag] | Any
    isEditable: bool
