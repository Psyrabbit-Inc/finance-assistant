from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.ui.screen_renderer import ScreenRenderer
from bot.ui.components import Header, Section, Divider, Card, StatRow, Badge

renderer = ScreenRenderer()


def confirm_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Подтвердить")],
            [KeyboardButton("Отмена")],
        ],
        resize_keyboard=True
    )


async def render_confirm_screen(message, user, category, amount, comment, op_type):
    """
    Экран подтверждения операции.
    """
    icon = "➖" if op_type == "expense" else "➕"
    op_title = "Расход" if op_type == "expense" else "Доход"

    header = Header(f"{icon} Подтверждение операции").render()

    card = Card([
        StatRow("Тип", op_title),
        StatRow("Категория", category.name),
        StatRow("Сумма", f"{amount:,.2f} ₸"),
        StatRow("Комментарий", comment if comment else "—"),
    ]).render()

    bottom_note = Section(
        "Проверь данные перед сохранением.\n"
        "Если хочешь изменить — нажми *Отмена*."
    ).render()

    return await renderer.render(
        message=message,
        text=header + card + Divider().render() + bottom_note,
        reply_markup=confirm_kb()
    )
