from aiogram import Dispatcher

# основные хендлеры
from .start import router as start_router
from .add_transaction import router as transaction_router
from .gamification import router as gamification_router
from .stats import router as stats_router

# онбординг
from .onboarding.steps import router as onboarding_router

from bot.middlewares.services import ServicesMiddleware

def setup_routers(dp: Dispatcher, services: dict):
    mw = ServicesMiddleware(services)

    for router in (
        start_router,
        onboarding_router,
        transaction_router,
        gamification_router,
        stats_router,
    ):
        router.message.middleware(mw)
        router.callback_query.middleware(mw)
        dp.include_router(router)
