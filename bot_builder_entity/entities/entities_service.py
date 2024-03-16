from sqlmodel import select, delete

from .schemas.entity_schema import Entity
from .schemas.option_schema import Option
from .schemas.synonym_schema import Synonym
from .dto.create_entity_dto import CreateEntityDto
from .dto.update_entity_dto import UpdateEntityDto
from .dto.delete_entity_dto import DeleteEntityDto
from ..deps.postgres_session import PostgresSessionDepend


class EntitiesService:
    def __init__(self, session: PostgresSessionDepend):
        self.session = session

    def find(self, user_id: str) -> list[Entity]:
        stmt = select(Entity).where(Entity.user_id == user_id)
        return self.session.exec(stmt).all()

    def create(self, create_entity_dto: CreateEntityDto, user_id: str) -> bool:
        options = []
        synonyms = []

        entity_raw = create_entity_dto.model_dump()
        entity = Entity(name=entity_raw["name"], user_id=user_id)

        for option_raw in entity_raw["options"]:
            option = Option(name=option_raw["name"], entity_id=entity.id)
            options.append(option)

            for synonym_raw in option_raw["synonyms"]:
                synonym = Synonym(name=synonym_raw["name"], option_id=option.id)
                synonyms.append(synonym)

        self.session.add(entity)
        self.session.add_all(options)
        self.session.add_all(synonyms)
        self.session.commit()

        return True

    def update(self, update_entity_dto: UpdateEntityDto) -> bool:
        entity_raw = update_entity_dto.model_dump()
        entity = self.session.exec(
            select(Entity).where(Entity.id == entity_raw["id"])
        ).first()
        entity.name = entity_raw["name"]
        options = []
        synonyms = []

        for option_raw in entity_raw["options"]:
            if option_raw["id"]:
                option = self.session.exec(
                    select(Option).where(Option.id == option_raw["id"])
                ).first()

                if option_raw["deleted"]:
                    self.session.exec(
                        delete(Synonym).where(Synonym.option_id == option.id)
                    )
                    self.session.delete(option)
                else:
                    option.name = option_raw["name"]
                    options.append(option)

                    for synonym_raw in option_raw["synonyms"]:
                        if synonym_raw["deleted"] and synonym_raw["id"]:
                            synonym = self.session.exec(
                                select(Synonym).where(Synonym.id == synonym_raw["id"])
                            ).first()
                            self.session.delete(synonym)

                        elif synonym_raw["id"] is None:
                            synonym = Synonym(
                                name=synonym_raw["name"], option_id=option.id
                            )
                            synonyms.append(synonym)

            elif option_raw["id"] is None:
                option = Option(name=option_raw["name"], entity_id=entity.id)
                options.append(option)

                for synonym_raw in option_raw["synonyms"]:
                    synonym = Synonym(name=synonym_raw["name"], option_id=option.id)
                    synonyms.append(synonym)

        self.session.add(entity)
        self.session.add_all(options)
        self.session.add_all(synonyms)
        self.session.commit()

        return True

    def delete(self, delete_entity_dto: DeleteEntityDto) -> bool:
        delete_entity_dto = delete_entity_dto.model_dump()

        for entity_id in delete_entity_dto["ids"]:
            entity = self.session.exec(
                select(Entity).where(Entity.id == entity_id)
            ).first()
            options = self.session.exec(
                select(Option).where(Option.entity_id == entity.id)
            ).all()

            self.session.exec(
                delete(Synonym).where(
                    Synonym.option_id.in_([option.id for option in options])
                )
            )

            for option in options:
                self.session.delete(option)

            self.session.delete(entity)

        self.session.commit()

        return True
