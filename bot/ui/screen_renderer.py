from typing import Optional, Union

from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup

from bot.ui.components.header import Header
from bot.ui.components.card import Card


class ScreenRenderer:
    async def render(
        self,
        message: Message,
        header: Optional[Header] = None,
        body: Optional[Card] = None,
        reply_markup: Optional[Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]] = None,
        screen_id: Optional[str] = None,
        user=None,
    ):
        parts = []

        if header:
            parts.append(header.render())

        if body:
            parts.append(body.render())

        text = "\n\n".join(parts)

        return await message.answer(
            text=text,
            reply_markup=reply_markup,
        )
