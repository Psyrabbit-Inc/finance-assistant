from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup


class ScreenRenderer:
    def __init__(self, user_repo=None):
        self.user_repo = user_repo

    async def render(
        self,
        message: Message,
        text: str,
        reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
        screen_id: str | None = None,
        user=None,
    ):
        if user and screen_id and self.user_repo:
            await self.user_repo.update_last_screen(user.id, screen_id)

        return await message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
