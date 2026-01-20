from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from infrastructure.db import async_session_maker
from infrastructure.models import Achievement


class AchievementRepository:

    async def exists(self, user_id: int, code: str) -> bool:
        """Проверка есть ли уже такая ачивка у пользователя"""
        async with async_session_maker() as session:
            query = select(Achievement).where(
                Achievement.user_id == user_id,
                Achievement.code == code
            )
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None

    async def add(self, user_id: int, code: str, name: str, description: str):
        """Создать новую ачивку"""
        async with async_session_maker() as session:
            achievement = Achievement(
                user_id=user_id,
                code=code,
                name=name,
                description=description,
                earned_at=datetime.utcnow()
            )
            session.add(achievement)
            await session.commit()
            return achievement

    async def get_all(self, user_id: int):
        """Все ачивки пользователя"""
        async with async_session_maker() as session:
            query = (
                select(Achievement)
                .where(Achievement.user_id == user_id)
                .order_by(Achievement.earned_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()
