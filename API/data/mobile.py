from __future__ import annotations

from typing import List, Optional

from API.data.config_class import BaseModel


###############################################   Поиск для мобильной апи


class ProductInMobilSearch(BaseModel):
    code: str
    name: str
    status: str
    type: str
    subtype: str
    productOwner: str
    mainProduct: str
    isArchive: bool


class SearchMobilItem(BaseModel):
    Priority: int
    Products: List[ProductInMobilSearch]


class MobilSearch(BaseModel):
    Mobile: List[SearchMobilItem]


###############################################  Продукт в мобильной АПИ

class ValueMobil(BaseModel):
    string: Optional[str] = None
    login: Optional[str] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    time: Optional[str] = None
    text: Optional[str] = None
    oracleCode: Optional[str] = None


class AttributeMobil(BaseModel):
    code: str
    name: str
    type: str
    values: List[ValueMobil]


class ProductMobil(BaseModel):
    code: int
    type: str
    name: str
    description: str
    attributes: List[AttributeMobil]


###############################################  Продукт в мобильной АПИ v2

class ValueMobilV2(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    oracleCode: Optional[str] = None
    time: Optional[str] = None
    login: Optional[str] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    link: Optional[str] = None
    string: Optional[str] = None
    text: Optional[str] = None


class AttributeMobilV2(BaseModel):
    code: str
    name: str
    type: str
    values: List[ValueMobilV2]
    reasonForDeletion: str


class ProductV2(BaseModel):
    type: str
    name: str
    description: str
    attributes: List[AttributeMobilV2]
    code: int




###############################################  Продукт в избранных

class FavProduct(BaseModel):
    code: str
    name: str
    status: str
    type: str
    subtype: str
    productOwner: str
    mainProduct: str
    isArchive: bool


class FavProductsList(BaseModel):
    products: List[FavProduct]


###############################################  Мои продукты

class ManagedProductsList(BaseModel):
    products: List[FavProduct]
