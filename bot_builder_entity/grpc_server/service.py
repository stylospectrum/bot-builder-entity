import json

from sqlmodel import Session, select

from ..proto.bot_builder_entity import (
    bot_builder_entity_pb2_grpc,
    bot_builder_entity_pb2,
)
from ..postgres.engine import engine
from ..entities.schemas.entity_schema import Entity
from .dto.entity_out_dto import EntityOutDto


class BotBuilderEntityServicer(
    bot_builder_entity_pb2_grpc.BotBuilderStoryServiceServicer
):
    def GetEntities(self, request, context):
        with Session(engine) as session:
            entities = session.exec(
                select(Entity).where(Entity.user_id == request.user_id)
            ).all()
            result = []

            for entity in entities:
                result.append(
                    json.loads(EntityOutDto.model_validate(entity).model_dump_json())
                )

            return bot_builder_entity_pb2.GetEntitiesResponse(entities=result)
