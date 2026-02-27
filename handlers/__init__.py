from .private import router as private_router
from .chs import router as chs_router
from .trips import router as trips_router
from .housing import router as housing_router
from .group import router as group_router
from .greeting import router as greeting_router
from .organizations import router as organizations_router
from .news import router as news_router
from .helpers import router as helpers_router
from .moderation import router as moderation_router
from .ads import router as ads_router
from .channel import router as channel_router
from .repost import router as repost_router

all_routers = [
    private_router,
    chs_router,
    trips_router,
    housing_router,
    group_router,
    greeting_router,
    organizations_router,
    news_router,
    helpers_router,
    moderation_router,
    ads_router,
    channel_router,
    repost_router
]