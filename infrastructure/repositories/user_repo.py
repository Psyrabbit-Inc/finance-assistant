from sqlalchemy import select, update
from infrastructure.db import async_session_maker
from infrastructure.models import User
from infrastructure.repositories.category_repo import CategoryRepository


class UserRepository:
    async def get_by_telegram_id(self, telegram_id: int):
        async with async_session_maker() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def create_if_not_exists(self, telegram_id: int) -> User:
        async with async_session_maker() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                return user

            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # добавляем дефолтные категории
        cat_repo = CategoryRepository()

        defaults = [
            ("Продукты", "expense"),
            ("Транспорт", "expense"),
            ("Развлечения", "expense"),
            ("Подписки", "expense"),
            ("Кафе", "expense"),
            ("Зарплата", "income"),
            ("Подарки", "income"),
            ("Продажи", "income"),
        ]

        for name, type_ in defaults:
            await cat_repo.create(user.id, name, type_)

        return user

    async def update(self, user: User):
        async with async_session_maker() as session:
            await session.execute(
                update(User)
                .where(User.id == user.id)
                .values(
                    xp=user.xp,
                    level=user.level,
                    streak_days=user.streak_days,
                    last_activity=user.last_activity,
                    is_onboarded=user.is_onboarded,
                    trust_score=user.trust_score,
                    last_screen_id=user.last_screen_id,
                )
            )
            await session.commit()

    async def update_trust(self, user_id: int, trust_score: float):
        async with async_session_maker() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(trust_score=trust_score)
            )
            await session.execute(stmt)
            await session.commit()

    async def update_screen(self, user_id: int, screen_id: str):
        async with async_session_maker() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(last_screen_id=screen_id)
            )
            await session.execute(stmt)
            await session.commit()