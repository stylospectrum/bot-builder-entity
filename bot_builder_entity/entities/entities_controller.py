from fastapi import Depends, Request

from .dto.create_entity_dto import CreateEntityDto
from .dto.entity_out_dto import EntityOutDto
from .dto.update_entity_dto import UpdateEntityDto
from .dto.delete_entity_dto import DeleteEntityDto
from ..core.controller import Controller, Get, Post, Delete, Put
from ..decorators.validate_token import validate_token
from ..deps.auth_service_stub import AuthServiceStubDepend
from ..entities.entities_service import EntitiesService


@Controller("entity")
class EntitiesController:
    entities_service: EntitiesService = Depends(EntitiesService)

    @Get("/", response_model=list[EntityOutDto])
    @validate_token
    def find(self, request: Request, auth_service_stub: AuthServiceStubDepend):
        user_id = request.__dict__["user"].id
        return self.entities_service.find(user_id)

    @Post("/")
    @validate_token
    def create(
        self,
        request: Request,
        auth_service_stub: AuthServiceStubDepend,
        create_entity_dto: CreateEntityDto,
    ):
        user_id = request.__dict__["user"].id
        return self.entities_service.create(create_entity_dto, user_id)

    @Put("/")
    @validate_token
    def update(
        self,
        request: Request,
        auth_service_stub: AuthServiceStubDepend,
        update_entity_dto: UpdateEntityDto,
    ):
        return self.entities_service.update(update_entity_dto)

    @Delete("/")
    @validate_token
    def delete(
        self,
        request: Request,
        auth_service_stub: AuthServiceStubDepend,
        delete_entity_dto: DeleteEntityDto,
    ):
        return self.entities_service.delete(delete_entity_dto)
