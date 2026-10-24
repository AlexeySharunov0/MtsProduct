from __future__ import annotations

from datetime import datetime
from uuid import UUID

from API.data.config_class import BaseModel


####### Получение инструмента по id

class Employee(BaseModel):
    avatar: str
    fullName: str
    isFired: bool
    login: str


class File(BaseModel):
    id: str
    link: str
    name: str
    size: int


class Link(BaseModel):
    name: str
    url: str


class Tool(BaseModel):
    createdAt: str
    description: str
    employees: list[Employee]
    files: list[File]
    group_id: str
    id: str
    isActive: bool
    links: list[Link]
    name: str
    tags: list[str]
    updatedAt: str


####### Получение группы инструментов по id

class ToolInGroup(BaseModel):
    id: UUID
    name: str
    description: str
    weight: int
    updated_at: datetime
    isActive: bool
    shortDescription: str

class Scheme(BaseModel):
    id: str
    name: str
    description: str


class ToolGroup(BaseModel):
    id: UUID
    groupName: str
    numImage: int
    tool: list[ToolInGroup]
    scheme: Scheme | None
    groupDescription: str
    links: list






####### Получение списка групп инструментов


class ToolGroupInList(BaseModel):
    count_tool: int
    description: str
    id: UUID
    name: str
    numImage: int
    weight: int


class ToolGroups(BaseModel):
    tool_groups: list[ToolGroupInList]
