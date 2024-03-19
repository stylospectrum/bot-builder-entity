import grpc
import logging

from concurrent import futures

from .service import BotBuilderEntityServicer
from ..proto.bot_builder_entity import bot_builder_entity_pb2_grpc
from ..config.settings import settings


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    bot_builder_entity_pb2_grpc.add_BotBuilderStoryServiceServicer_to_server(
        BotBuilderEntityServicer(), server
    )
    server.add_insecure_port(f"[::]:{settings.SERVICE_URL}")
    server.start()

    logging.basicConfig(level=logging.INFO)
    logging.info("gRPC server running...")

    return server
