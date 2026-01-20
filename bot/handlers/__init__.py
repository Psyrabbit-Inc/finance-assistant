from aiogram import Dispatcher

# основные хендлеры
from .start import router as start_router
from .add_transaction import router as transaction_router
from .gamification import router as gamification_router
from .stats import router as stats_router

# онбординг
from .onboarding.steps import router as onboarding_router


def setup_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(onboarding_router)
    dp.include_router(transaction_router)
    dp.include_router(gamification_router)
    dp.include_router(stats_router)
