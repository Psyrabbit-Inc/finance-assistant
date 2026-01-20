from bot.ui.screen_renderer import ScreenRenderer
from bot.keyboards.main_menu import main_menu_kb

from bot.ui.components import Header, Card, StatRow, Badge


async def render_main_screen(message, user):
    renderer = ScreenRenderer()

    profile_card = Card([
        Badge("👤", user.nickname or "Пользователь"),
        StatRow("🏆", "Уровень", user.level),
        StatRow("⭐", "XP", user.xp),
        StatRow("🔥", "Стрик", f"{user.streak_days} дней"),
    ])

    text = (
        Header("Личный кабинет").render() +
        profile_card.render() +
        "Выбери действие ниже 👇"
    )

    return await renderer.render(
        message=message,
        text=text,
        reply_markup=main_menu_kb()
    )