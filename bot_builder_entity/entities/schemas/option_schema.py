import uuid

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .entity_schema import Entity
    from .synonym_schema import Synonym


class Option(SQLModel, table=True):
    __tablename__ = "option"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True)
    entity_id: uuid.UUID = Field(foreign_key="entity.id")
    name: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)

    entity: Optional['Entity'] = Relationship(back_populates="options")
    synonyms: Optional[list['Synonym']] = Relationship(
        back_populates="option")
