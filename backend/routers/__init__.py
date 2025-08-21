# CRM\backend\__init__.py
from .users import router as users_router
from .clients import router as clients_router
from .tasks import router as tasks_router
from .payments import router as payments_router

all_routers = [
    users_router,
    clients_router,
    tasks_router,
    payments_router,
]
