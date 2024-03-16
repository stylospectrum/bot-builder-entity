import uuid

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .option_schema import Option


class Synonym(SQLModel, table=True):
    __tablename__ = "synonym"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    option_id: uuid.UUID = Field(foreign_key="option.id")
    name: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    option: Optional["Option"] = Relationship(back_populates="synonyms")
