from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def onboarding_next_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Дальше ▶️")],
            [KeyboardButton(text="Пропустить ⏭")],
        ],
        resize_keyboard=True
    )

def onboarding_finish_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Завершить ✅")],
            [KeyboardButton(text="Пропустить ⏭")],
        ],
        resize_keyboard=True
    )
