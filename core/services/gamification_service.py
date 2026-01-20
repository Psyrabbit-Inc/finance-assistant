from datetime import datetime, timedelta
from math import sqrt

from infrastructure.db import async_session_maker
from infrastructure.models import User
from core.services.trust_service import TrustService


class GamificationService:
    XP_PER_TRANSACTION = 10
    XP_PER_STREAK_DAY = 25

    def __init__(self):
        self.trust = TrustService()

    def calculate_level(self, xp: int) -> int:
        """ Формула прогрессии уровня """
        return int(sqrt(xp / 50)) + 1

    async def process_transaction(self, user: User):
        """
        Обновляет:
          — XP (+ множитель от Trust Score)
          — Streak (правильно)
          — Level
          — Дату последней активности
        Возвращает:
          level, streak_days, total_xp, earned_xp
        """

        async with async_session_maker() as session:
            db_user = await session.get(User, user.id)

            now = datetime.utcnow().date()

            # ---------------------------------------------------------
            # 1. Проверяем дату последней активности
            # ---------------------------------------------------------
            last_activity = (
                db_user.last_activity.date()
                if db_user.last_activity
                else None
            )

            # Начинаем streak
            if last_activity is None:
                db_user.streak_days = 1
            else:
                # вчера → streak продолжается
                if last_activity == now - timedelta(days=1):
                    db_user.streak_days += 1
                # сегодня → streak не меняем
                elif last_activity == now:
                    pass
                # пропуск → streak сброшен
                else:
                    db_user.streak_days = 1

            # ---------------------------------------------------------
            # 2. Начисление XP за транзакцию (основное)
            # ---------------------------------------------------------
            base_xp = self.XP_PER_TRANSACTION
            multiplier = self.trust.xp_multiplier(db_user.trust_score)
            earned_xp = int(base_xp * multiplier)

            db_user.xp += earned_xp

            # ---------------------------------------------------------
            # 3. XP за streak
            # ---------------------------------------------------------
            streak_xp = int(self.XP_PER_STREAK_DAY * multiplier)
            db_user.xp += streak_xp

            # ---------------------------------------------------------
            # 4. Обновляем дату последней активности
            # ---------------------------------------------------------
            db_user.last_activity = datetime.utcnow()

            # ---------------------------------------------------------
            # 5. Пересчитываем уровень
            # ---------------------------------------------------------
            db_user.level = self.calculate_level(db_user.xp)

            await session.commit()
            await session.refresh(db_user)

            # Возвращаем только то, что ожидает вызывающий код
            return db_user.level, db_user.streak_days, db_user.xp

    async def add_xp(self, user: User, xp_amount: int, reason: str | None = None):
        """
        Начисление XP не как транзакции, а как награды:
        - за онбординг
        - за ачивки
        - за обучение
        - за задания
        """

        async with async_session_maker() as session:
            db_user = await session.get(User, user.id)

            # Множитель доверия
            multiplier = self.trust.xp_multiplier(db_user.trust_score)

            earned_xp = int(xp_amount * multiplier)
            db_user.xp += earned_xp

            # Пересчитываем уровень
            db_user.level = self.calculate_level(db_user.xp)

            # Не трогаем streak!
            # Это важно: онбординг не должен ломать или начинать streak.

            await session.commit()
            await session.refresh(db_user)

            return db_user.level, db_user.streak_days, db_user.xp

