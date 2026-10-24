from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from API.data.config_class import BaseModel


###############################################  Кеш категории


class ValueCategory(BaseModel):
    code: str
    value: str


class PropertyCategory(BaseModel):
    code: str
    values: list[ValueCategory]


class ProductInCategory(BaseModel):
    code: str
    name: str
    properties: Any


class Category(BaseModel):
    code: str
    name: str
    type: str
    products: list[ProductInCategory]
    count: int


class Categories(BaseModel):
    categories: list[Category]


###############################################   Тотал

class Total(BaseModel):
    product: int
    archive: int
    hub: int


###############################################   Каунтер


class ValueCounter(BaseModel):
    code: str
    value: str
    count: int


class CounterItem(BaseModel):
    code: str
    name: str
    description: str
    values: list[ValueCounter]
    total: int
    weight: int


class Counter(BaseModel):
    counter: list[CounterItem]


###############################################   Фильтр

class Product(BaseModel):
    code: str
    name: str
    properties: Properties


class FilterValue(BaseModel):
    code: str
    count: int
    value: str


class FilterItem(BaseModel):
    code: str
    name: str
    total: int
    description: str
    values: list[FilterValue]
    weight: int


class Filter(BaseModel):
    categories: list[Category]
    filters: list[FilterItem]


###############################################   Новые Продукты

class TipObieektaUcheta(BaseModel):
    code: str
    count: int
    value: str

class NapravlenieGruppy(BaseModel):
    code: str
    count: int
    value: str


class RD(BaseModel):
    code: str
    count: int
    value: str


class PPinfoStatus(BaseModel):
    code: str
    value: str
    count: int


class Properties(BaseModel):
    employee_product_owner: Optional[str] = None
    PPinfo_status: PPinfoStatus
    SYSTEM_ProductType: str
    isNew: bool
    isBrand: Optional[bool] = None
    isInitClose: Optional[bool] = None
    isArchive: Optional[bool] = None
    PPInfo_main_product: Optional[str] = None
    Napravlenie_gruppy: Optional[NapravlenieGruppy] = None
    R_D: Optional[RD] = Field(None, alias='R&D')
    Tip_obieekta_ucheta: Optional[TipObieektaUcheta] = None



class PropertiesClose(BaseModel):
    PPinfo_status: PPinfoStatus
    SYSTEM_ProductType: str
    isArchive: Optional[bool] = None
    PPInfo_main_product: Optional[str] = None
    isInitClose: Optional[bool] = None
    employee_product_owner: Optional[str] = None
    isNew: Optional[bool] = None
    isBrand: Optional[bool] = None
    isEcosystemProduct: Optional[bool] = None
    Napravlenie_gruppy: Optional[NapravlenieGruppy] = None
    R_D: Optional[RD] = Field(None, alias='R&D')
    Tip_obieekta_ucheta: Optional[TipObieektaUcheta] = None



class NewItem(BaseModel):
    code: str
    name: str
    properties: Properties


class CloseItem(BaseModel):
    code: str
    name: str
    properties: PropertiesClose

class IdeaItem(BaseModel):
    code: str
    name: str
    properties: PropertiesClose


class New(BaseModel):
    news: list[NewItem]


class Close(BaseModel):
    close: list[CloseItem]

class Idea(BaseModel):
    idea: list[IdeaItem]
