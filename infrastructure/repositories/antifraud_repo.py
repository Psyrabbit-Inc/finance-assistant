from datetime import datetime, timedelta
from sqlalchemy import select, func
from infrastructure.db import async_session_maker
from infrastructure.models import AntiFraud


class AntiFraudRepository:

    async def log(self, user_id: int, action_type: str, amount: float | None = None):
        async with async_session_maker() as session:
            event = AntiFraud(
                user_id=user_id,
                action_type=action_type,
                amount=amount
            )
            session.add(event)
            await session.commit()

    async def count_recent(self, user_id: int, action_type: str, minutes: int = 1) -> int:
        """
        Считает количество событий за последние N минут.
        Работает одинаково и в SQLite, и в Postgres.
        """
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)

        async with async_session_maker() as session:
            stmt = (
                select(func.count())
                .where(
                    AntiFraud.user_id == user_id,
                    AntiFraud.action_type == action_type,
                    AntiFraud.created_at >= cutoff,
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one()
