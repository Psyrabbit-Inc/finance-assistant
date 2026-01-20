from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()  # грузим .env

@dataclass
class BotConfig:
    token: str

@dataclass
class DBConfig:
    url: str  # например, "sqlite+aiosqlite:///./finance.db"

@dataclass
class Config:
    bot: BotConfig
    db: DBConfig


def load_config() -> Config:
    return Config(
        bot=BotConfig(
            token=os.getenv("BOT_TOKEN", "")
        ),
        db=DBConfig(
            url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./finance.db")
        ),
    )
