from sqlmodel import SQLModel

class DeleteEntityDto(SQLModel):
  ids: list[str] = []