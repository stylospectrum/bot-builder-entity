import uuid

from sqlmodel import SQLModel
from typing import Optional


class SynonymDto(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    deleted: Optional[bool] = False


class OptionDto(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    deleted: Optional[bool] = False
    synonyms: Optional[list[SynonymDto]] = []


class EntityBaseDto(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    options: Optional[list[OptionDto]] = []
