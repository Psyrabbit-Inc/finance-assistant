from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="➕ Добавить расход"),
            KeyboardButton(text="💰 Добавить доход"),
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="🏅 Мой уровень"),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
