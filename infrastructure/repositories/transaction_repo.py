from datetime import datetime
from typing import List

from sqlalchemy import select

from infrastructure.db import async_session_maker
from infrastructure.models import Transaction, TransactionType


class TransactionRepository:

    async def add_transaction(
        self,
        user_id: int,
        type_: TransactionType,
        amount: float,
        category_id: int,
        comment: str | None
    ) -> Transaction:

        async with async_session_maker() as session:
            tx = Transaction(
                user_id=user_id,
                type=type_,
                amount=amount,
                category_id=category_id,
                comment=comment
            )
            session.add(tx)
            await session.commit()
            await session.refresh(tx)
            return tx

    async def get_for_period(
        self,
        user_id: int,
        start: datetime,
        end: datetime
    ) -> List[Transaction]:
        async with async_session_maker() as session:
            stmt = (
                select(Transaction)
                .where(Transaction.user_id == user_id)
                .where(Transaction.created_at >= start)
                .where(Transaction.created_at < end)
            )
            res = await session.execute(stmt)
            return res.scalars().all()
