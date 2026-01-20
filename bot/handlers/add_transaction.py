from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.add_transaction import AddTransactionState
from bot.keyboards.main_menu import main_menu_kb

from infrastructure.models import TransactionType
from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.category_repo import CategoryRepository
from infrastructure.repositories.transaction_repo import TransactionRepository

from core.services.gamification_service import GamificationService
from core.services.achievement_service import AchievementService
from core.services.antifraud_service import AntiFraudService

# UI COMPONENTS
from bot.ui.screen_renderer import ScreenRenderer
from bot.ui.components.header import Header
from bot.ui.components.card import Card
from bot.ui.components.section import Section
from bot.ui.components.badge import Badge
from bot.ui.components.divider import Divider
from bot.ui.components.layout import VStack

router = Router()

renderer = ScreenRenderer()
user_repo = UserRepository()
cat_repo = CategoryRepository()
tx_repo = TransactionRepository()

gamification = GamificationService()
achievement_service = AchievementService()
antifraud = AntiFraudService()


# ============================================================
#             ШАГ 1 — старт (выбор расхода/дохода)
# ============================================================

@router.message(F.text == "➕ Добавить расход")
async def add_expense(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(tx_type="expense")
    await state.set_state(AddTransactionState.waiting_for_amount)

    await renderer.render(
        message,
        screen_id="enter_amount",
        header=Header("🧾 Добавляем расход"),
        body=Card(
            "Введи сумму, например: 1500 или 1500.50\n"
            "Чтобы отменить — напиши <b>отмена</b>."
        ),
    )


@router.message(F.text == "💰 Добавить доход")
async def add_income(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(tx_type="income")
    await state.set_state(AddTransactionState.waiting_for_amount)

    await renderer.render(
        message,
        screen_id="enter_amount",
        header=Header("💰 Добавляем доход"),
        body=Card(
            "Введи сумму, например: 20000\n"
            "Чтобы отменить — напиши <b>отмена</b>."
        ),
    )


# ============================================================
#             ШАГ 2 — ввод суммы (A3.3 UI)
# ============================================================

@router.message(AddTransactionState.waiting_for_amount)
async def amount_entered(message: Message, state: FSMContext):
    text = message.text.lower().strip()

    # Отмена
    if text in ("отмена", "cancel", "❌"):
        await state.clear()
        await message.answer("Окей, отменил 🙂", reply_markup=main_menu_kb())
        return

    # Валидация суммы
    try:
        amount = float(text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        # UI-ошибка
        await renderer.render(
            message,
            screen_id="amount_invalid",
            header=Header("⚠️ Некорректная сумма"),
            body=Card(
                "Сумма должна быть числом больше 0.\n"
                "Попробуй снова 🙂"
            ),
        )
        return

    await state.update_data(amount=amount)

    user = await user_repo.get_by_telegram_id(message.from_user.id)

    # Загружаем категории под конкретный тип
    data = await state.get_data()
    tx_type = data["tx_type"]

    categories = await cat_repo.get_all(user.id)
    categories = [c for c in categories if c.type == tx_type]

    if not categories:
        await message.answer("Нет категорий для этого типа 😕", reply_markup=main_menu_kb())
        await state.clear()
        return

    await state.set_state(AddTransactionState.waiting_for_category)

    # 👇 UI — экран выбора категории
    rows = []
    for c in categories:
        rows.append(
            Badge(c.name, callback_data=f"cat:{c.id}")
        )

    body = VStack(
       Section("Выбери категорию:"),
        *rows,
        Divider(),
        Badge("❌ Отменить", callback_data="cancel_tx")
    )

    return await renderer.render(
        message,
        screen_id="choose_category",
        header=Header("📂 Выбор категории"),
        body=Card(body),
    )


# ============================================================
#             ШАГ 3 — выбор категории (A3.2 UI)
# ============================================================

@router.callback_query(AddTransactionState.waiting_for_category, F.data == "cancel_tx")
async def cancel_from_categories(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer("Окей, отменил 🙂", reply_markup=main_menu_kb())


@router.callback_query(AddTransactionState.waiting_for_category, F.data.startswith("cat:"))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split(":")[1])

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    category = await cat_repo.get_by_id(cat_id, user.id)

    if category is None:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    await state.update_data(category_id=cat_id, category_name=category.name)
    await state.set_state(AddTransactionState.waiting_for_comment)

    await callback.answer()

    # Переход к вводу комментария
    await callback.message.answer(
        "Если хочешь, добавь комментарий.\n"
        "Или напиши <b>-</b>, чтобы пропустить.\n"
        "Для отмены — <b>отмена</b>."
    )


# ============================================================
#             ШАГ 4 — комментарий → сохранение
# ============================================================

@router.message(AddTransactionState.waiting_for_comment)
async def comment_entered(message: Message, state: FSMContext):
    text = message.text.strip().lower()

    # отмена
    if text in ("отмена", "cancel", "❌"):
        await state.clear()
        await message.answer("Окей, ничего не добавил 🙂", reply_markup=main_menu_kb())
        return

    comment = None if text == "-" else message.text

    data = await state.get_data()
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    tx_type = TransactionType(data["tx_type"])
    amount = data["amount"]
    category_id = data["category_id"]
    category_name = data["category_name"]

    # сохраняем транзакцию
    await tx_repo.add_transaction(
        user_id=user.id,
        type_=tx_type,
        amount=amount,
        category_id=category_id,
        comment=comment,
    )

    await state.clear()

    # антифрод
    fraud_ok = await antifraud.validate_transaction(user, amount)

    if not fraud_ok:
        await message.answer(
            "⚠️ <b>Подозрительная активность</b>\n"
            "XP не начислено."
        )
        return await message.answer("Продолжим? 👇", reply_markup=main_menu_kb())

    # начисление XP
    level, streak, xp = await gamification.process_transaction(user)

    await message.answer(
        f"💵 <b>Запись добавлена!</b>\n\n"
        f"Сумма: <b>{amount}</b>\n"
        f"Категория: <b>{category_name}</b>\n"
        f"Комментарий: <i>{comment or '—'}</i>\n\n"
        f"✨ +{GamificationService.XP_PER_TRANSACTION} XP\n"
        f"🔥 Streak: {streak} дней\n"
        f"🏅 Уровень: {level}\n"
        f"📊 XP: {xp}",
        reply_markup=main_menu_kb()
    )
