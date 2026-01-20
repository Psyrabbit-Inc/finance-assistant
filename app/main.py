import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import load_config

from infrastructure.db import init_db
from bot.handlers import setup_routers


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

    config = load_config()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher()

    # ⬇️ ПРАВИЛЬНОЕ МЕСТО
    setup_routers(dp)

    logger.info("Initializing DB...")
    await init_db()

    logger.info("Bot started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
