import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import load_config

from infrastructure.db import init_db
from bot.handlers import setup_routers
from bot.ui.screen_renderer import ScreenRenderer

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.transaction_repo import TransactionRepository
from infrastructure.repositories.category_repo import CategoryRepository
from core.services.antifraud_service import AntiFraudService
from core.services.gamification_service import GamificationService
from core.services.onboarding_service import OnboardingService


async def main():
    logging.basicConfig()
    logger = logging.getLogger(__name__)

    config = load_config()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher()

    logger.info("Initializing DB...")
    await init_db()

    # ⬇️ COMPOSITION ROOT
    user_repo = UserRepository()
    tx_repo = TransactionRepository()
    antifraud = AntiFraudService()
    gamification = GamificationService()

    services = {
        "renderer": ScreenRenderer(),
        "user_repo": UserRepository(),
        "tx_repo": TransactionRepository(),
        "antifraud": AntiFraudService(),
        "gamification": GamificationService(),
        "onboarding_service": OnboardingService(),
        "cat_repo": CategoryRepository(),
    }

    setup_routers(dp, services)

    logger.info("Bot started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
