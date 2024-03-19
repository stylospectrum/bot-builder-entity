import threading
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import settings
from .core.core_module import CoreModule
from .grpc_server.module import serve_grpc
from .entities.entities_module import EntitiesModule
from .postgres.engine import create_db_and_tables
from .interceptors.response_interceptor import ResponseInterceptor

create_db_and_tables()

grpc_server = None


async def startup():
    global grpc_server
    grpc_server = serve_grpc()
    threading.Thread(target=grpc_server.wait_for_termination).start()


async def shutdown():
    global grpc_server
    if grpc_server is not None:
        grpc_server.stop(0)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = CoreModule(
    modules=[EntitiesModule],
    lifespan=lifespan,
)
app.add_middleware(ResponseInterceptor)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    uvicorn.run(
        "bot_builder_entity.main:app",
        host="0.0.0.0",
        port=int(settings.PORT),
        reload=True,
    )
