from .entities_service import EntitiesService
from .entities_controller import EntitiesController

class EntitiesModule:
    controllers = [EntitiesController]
    services = [EntitiesService]