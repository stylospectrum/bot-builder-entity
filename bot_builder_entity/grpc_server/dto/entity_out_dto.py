import uuid

from sqlmodel import SQLModel
from typing import Optional


class SynonymDto(SQLModel):
    name: Optional[str] = None


class OptionDto(SQLModel):
    name: Optional[str] = None
    synonyms: Optional[list[SynonymDto]] = []


class EntityOutDto(SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    options: Optional[list[OptionDto]] = []
