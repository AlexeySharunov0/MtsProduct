from pydantic import Field
from API.data.config_class import BaseModel
from typing import Any, List, Optional


class From(BaseModel):
    relays: Optional[List[str]] = []
    mailbox: Optional[str] = ''
    domain: Optional[str] = ''
    params: Optional[str] = ''


class ToItem(BaseModel):
    relays: Optional[List[str]] = []
    mailbox: Optional[str] = ''
    domain: Optional[str] = ''
    params: Optional[str] = ''


class Headers(BaseModel):
    content__transfer__encoding: list[str] = Field(..., alias='Content-Transfer-Encoding')
    content__type: list[str] = Field(..., alias='Content-Type')
    date: list[str] = Field(..., alias='Date')
    from_: list[str] = Field(..., alias='From')
    mime__version: list[str] = Field(..., alias='MIME-Version')
    message__id: list[str] = Field(..., alias='Message-ID')
    received: list[str] = Field(..., alias='Received')
    return__path: list[str] = Field(..., alias='Return-Path')
    subject: list[str] = Field(..., alias='Subject')
    to: list[str] = Field(..., alias='To')
    mime: Any = Field(..., alias='MIME')
    size: int = Field(..., alias="Size")


class Content(BaseModel):
    headers: Headers = Field(..., alias='Headers')
    body: str = Field(..., alias='Body')
    mime: Any = Field(..., alias='MIME')
    size: int = Field(..., alias="Size")


class Raw(BaseModel):
    from_: str = Field(..., alias='From')
    to: list[str] = Field(..., alias='To')
    data: str = Field(..., alias='Data')
    helo: str = Field(..., alias='Helo')


class Message(BaseModel):
    content: Content = Field(..., alias='Content')
    created: str = Field(..., alias='Created')
    from_: From | None = Field(..., alias='From')
    id: str = Field(..., alias='ID')
    mime: Any = Field(..., alias='MIME')
    raw: Raw = Field(..., alias='Raw')
    to: list[ToItem] | None = Field(..., alias='To')


class Messages(BaseModel):
    total: int
    start: int
    count: int
    items: list[Message]

