from typing import List, Optional
from sqlalchemy import select

from infrastructure.db import async_session_maker
from infrastructure.models import Category


class CategoryRepository:

    async def get_all(self, user_id: int) -> List[Category]:
        async with async_session_maker() as session:
            stmt = select(Category).where(Category.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def create(self, user_id: int, name: str, type_: str) -> Category:
        async with async_session_maker() as session:
            cat = Category(user_id=user_id, name=name, type=type_)

            session.add(cat)
            await session.commit()
            await session.refresh(cat)
            return cat

    async def get_by_id(self, category_id: int, user_id: int) -> Optional[Category]:
        async with async_session_maker() as session:
            stmt = select(Category).where(
                Category.id == category_id,
                Category.user_id == user_id
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
