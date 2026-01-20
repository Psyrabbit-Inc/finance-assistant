from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from infrastructure.models import Category


def categories_keyboard(categories: list[Category]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for cat in categories:
        rows.append(
            [InlineKeyboardButton(text=cat.name, callback_data=f"cat:{cat.id}")]
        )

    # ряд с отменой
    rows.append(
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_tx")]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)
