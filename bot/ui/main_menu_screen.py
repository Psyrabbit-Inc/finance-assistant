from bot.ui.components import Header, Card, StatRow, Badge, Text
from bot.keyboards.main_menu import main_menu_kb
from bot.ui.screen_renderer import ScreenRenderer


async def render_main_screen(message, user, renderer: ScreenRenderer):
    header = Header("🏠 Личный кабинет")

    body = Card([
        Badge("👤", user.nickname or "Пользователь"),
        StatRow("🏆", "Уровень", user.level),
        StatRow("⭐", "XP", user.xp),
        StatRow("🔥", "Стрик", f"{user.streak_days} дней"),
        Text("Выбери действие ниже 👇"),
    ])

    return await renderer.render(
        message=message,
        header=header,
        body=body,
        reply_markup=main_menu_kb()
    )
