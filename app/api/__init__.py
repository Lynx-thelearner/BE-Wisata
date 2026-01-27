from .user import user_router
from .auth import auth_router
from .wisata import wisata_router
from .category import category_router
from .tags import tags_router

routers = [
    user_router.router,
    auth_router.router,
    wisata_router.router,
    category_router.router,
    tags_router.router
]
