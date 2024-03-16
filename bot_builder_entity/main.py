import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from .config.settings import settings
from .core.core_module import CoreModule

from .entities.entities_module import EntitiesModule
from .postgres.engine import create_db_and_tables
from .interceptors.response_interceptor import ResponseInterceptor

create_db_and_tables()

app = CoreModule(modules=[EntitiesModule])
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
