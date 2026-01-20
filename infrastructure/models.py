from datetime import datetime
from sqlalchemy import (
    Integer,
    BigInteger,
    DateTime,
    String,
    ForeignKey,
    Enum,
    Float
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean
from sqlalchemy import DateTime, Float, Integer, String, ForeignKey, func



from .db import Base
import enum


class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)

    # relations
    categories: Mapped[list["Category"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")

    # onboarding
    is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False)

    # antifraud
    trust_score: Mapped[int] = mapped_column(Integer, default=100)

    last_activity: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    last_screen_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    nickname: Mapped[str | None] = mapped_column(String(64), nullable=True)

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(16))  # "income" или "expense"

    user: Mapped["User"] = relationship(back_populates="categories")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    amount: Mapped[float] = mapped_column(Float)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship()


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[str] = mapped_column(String(64))   # уникальный код ачивки
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(255))
    earned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AntiFraud(Base):
    __tablename__ = "antifraud"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action_type: Mapped[str] = mapped_column(String(64))
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,  # Python default
        server_default=func.now(),  # SQL default
        nullable=False
    )