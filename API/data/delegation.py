from __future__ import annotations

from typing import List

from API.data.config_class import BaseModel


###############################################   Делагирование

class ManagerItemDelegation(BaseModel):
    login: str
    fullname: str
    avatar: str


class ProductDelegation(BaseModel):
    Id: str
    code: str
    name: str


class Delegation(BaseModel):
    id: str
    manager: str | ManagerItemDelegation | None
    executer: str | ManagerItemDelegation | None
    product: ProductDelegation


class Delegations(BaseModel):
    delegations: List[Delegation]
