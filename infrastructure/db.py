from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import load_config

config = load_config()

class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    config.db.url,
    echo=False,
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def init_db():
    from . import models  # важно!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
