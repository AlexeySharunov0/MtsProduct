from __future__ import annotations

from typing import List, Any, Optional

from pydantic import Field

from API.data.config_class import BaseModel


###############################################   Поиск новый

class Highlight(BaseModel):
    name: Optional[dict[str, Any]] = None
    tag: Optional[dict[str, Any]] = None
    applications_names: Optional[dict[str, Any]] = None
    applications_codes: Optional[dict[str, Any]] = None
    info_system_names: Optional[dict[str, Any]] = None
    info_system_teams: Optional[dict[str, Any]] = None
    oldName: Optional[dict[str, Any]] = None
    window: Optional[dict[str, Any]] = None
    oracleCode: Optional[dict[str, Any]] = None
    code_keyword: Optional[dict[str, Any]] = Field(None, alias='code.keyword')
    fioEmployees: Optional[dict[str, Any]] = None
    loginEmployees: Optional[dict[str, Any]] = None
    names_realizes_service: Optional[dict[str, Any]] = None
    names_served_service: Optional[dict[str, Any]] = None
    codes_realizes_service: Optional[dict[str, Any]] = None



class NapravlenieGruppy(BaseModel):
    code: str
    value: str


class PPinfoStatus(BaseModel):
    code: str
    value: str


class RD(BaseModel):
    code: str
    value: str


class TipObieektaUcheta(BaseModel):
    code: str
    value: str


class Properties(BaseModel):
    Napravlenie_gruppy: Optional[NapravlenieGruppy] = None
    PPinfo_status: PPinfoStatus
    R_D: Optional[RD] = Field(None, alias='R&D')
    SYSTEM_ProductType: str
    Tip_obieekta_ucheta: Optional[TipObieektaUcheta] = None
    employee_product_owner: Optional[str] = None
    PPInfo_main_product: Optional[str] = None
    isNew: Optional[bool] = None
    isInitClose: Optional[bool] = None
    isArchive: Optional[bool] = None
    isDeleted: Optional[bool] = None
    isKhab: Optional[bool] = None
    Kategoriia_khaba: Optional[TipObieektaUcheta] = None


class ProductInSearch(BaseModel):
    code: str
    name: str
    highlight: Highlight
    properties: Properties


class SearchModel(BaseModel):
    search: List[ProductInSearch]

###############################################   Подсказки


class GroupName(BaseModel):
    code: str
    value: str


class ObjectType(BaseModel):
    code: str
    value: str


class Suggestion(BaseModel):
    code: str
    name: str
    type: str
    isKhab: bool
    groupName: GroupName
    objectType: ObjectType
    isStatusArchive: bool
    isDeleted: bool


class Suggestions(BaseModel):
    suggestions: List[Suggestion]


###############################################   Поиск новый


class Product(BaseModel):
    name: str
    code: str


class NewSearchResult(BaseModel):
    search_result: List[Product]
