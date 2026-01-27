from decimal import Decimal, InvalidOperation

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.add_transaction import AddTransactionState
from bot.keyboards.main_menu import main_menu_kb
from bot.keyboards.categories import categories_keyboard  # ❗ важно

from bot.ui.screen_renderer import ScreenRenderer
from bot.ui.components import Header, Card, Text, StatRow, Divider

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.category_repo import CategoryRepository
from infrastructure.repositories.transaction_repo import TransactionRepository

from core.services.antifraud_service import AntiFraudService
from core.services.gamification_service import GamificationService
from core.services.achievement_service import AchievementService

router = Router()

# ───────────────────────────────
# ENTRY
# ───────────────────────────────

@router.message(F.text == "➕ Добавить расход")
async def add_expense(message: Message, state: FSMContext, renderer: ScreenRenderer):
    await state.clear()
    await state.set_state(AddTransactionState.waiting_for_amount)
    await state.update_data(tx_type="expense")

    await renderer.render(
        message=message,
        header=Header("➕ Добавление расхода"),
        body=Card([
            Text("Введи сумму, например: 1500 или 1500.50"),
            Text("Чтобы отменить — напиши <b>отмена</b>."),
        ]),
    )


@router.message(F.text == "💰 Добавить доход")
async def add_income(message: Message, state: FSMContext, renderer: ScreenRenderer):
    await state.clear()
    await state.set_state(AddTransactionState.waiting_for_amount)
    await state.update_data(tx_type="income")

    await renderer.render(
        message=message,
        header=Header("💰 Добавление дохода"),
        body=Card([
            Text("Введи сумму, например: 1500 или 1500.50"),
            Text("Чтобы отменить — напиши <b>отмена</b>."),
        ]),
    )


# ───────────────────────────────
# AMOUNT
# ───────────────────────────────

@router.message(AddTransactionState.waiting_for_amount)
async def amount_entered(
    message: Message,
    state: FSMContext,
    renderer: ScreenRenderer,
    cat_repo: CategoryRepository,
):
    text = message.text.strip().lower()

    if text in {"отмена", "cancel", "❌"}:
        await state.clear()
        await message.answer("Ок, отменили 👌", reply_markup=main_menu_kb())
        return

    try:
        amount = Decimal(message.text.replace(",", "."))
        if amount <= 0:
            raise InvalidOperation
    except (InvalidOperation, ValueError):
        await message.answer("❌ Введи корректную сумму")
        return

    await state.update_data(amount=amount)
    await state.set_state(AddTransactionState.waiting_for_category)

    categories = await cat_repo.get_all(message.from_user.id)

    await renderer.render(
        message=message,
        header=Header("📂 Категория"),
        body=Card([Text("Выбери категорию:")]),
        reply_markup=categories_keyboard(categories),
    )


# ───────────────────────────────
# CATEGORY
# ───────────────────────────────

@router.callback_query(AddTransactionState.waiting_for_category)
async def category_selected(
    call: CallbackQuery,
    state: FSMContext,
    cat_repo: CategoryRepository,
    renderer: ScreenRenderer,
):
    await call.answer()

    category = await cat_repo.get_by_id(call.data)
    if not category:
        await call.message.answer("❌ Категория не найдена")
        return

    await state.update_data(
        category_id=category.id,
        category_name=category.name,
    )
    await state.set_state(AddTransactionState.waiting_for_comment)

    await renderer.render(
        message=call.message,
        header=Header("✏️ Комментарий"),
        body=Card([
            Text("Добавь комментарий (необязательно)."),
            Text("Если не нужен — напиши <b>-</b>."),
        ]),
    )


# ───────────────────────────────
# COMMENT
# ───────────────────────────────

@router.message(AddTransactionState.waiting_for_comment)
async def comment_entered(message: Message, state: FSMContext, renderer: ScreenRenderer):
    text = message.text.strip()

    if text.lower() in {"отмена", "cancel", "❌"}:
        await state.clear()
        await message.answer("Ок, отменили 👌", reply_markup=main_menu_kb())
        return

    data = await state.get_data()
    comment = None if text == "-" else text

    await state.update_data(comment=comment)
    await state.set_state(AddTransactionState.waiting_for_confirm)

    await renderer.render(
        message=message,
        header=Header("✅ Подтверждение"),
        body=Card([
            StatRow("Тип", "Расход" if data["tx_type"] == "expense" else "Доход"),
            StatRow("Категория", data["category_name"]),
            StatRow("Сумма", f"{data['amount']:.2f}"),
            StatRow("Комментарий", comment or "—"),
            Divider(),
            Text("Подтвердить операцию?"),
        ]),
    )


# ───────────────────────────────
# CONFIRM/CANCEL
# ───────────────────────────────

@router.message(AddTransactionState.waiting_for_confirm)
async def confirm_transaction(
    message: Message,
    state: FSMContext,
    user_repo: UserRepository,
    tx_repo: TransactionRepository,
    antifraud: AntiFraudService,
    gamification: GamificationService,
    achievement_service: AchievementService,
):
    text = message.text.strip().lower()

    if text in {"отмена", "cancel", "❌"}:
        await state.clear()
        await message.answer("Операция отменена 👌", reply_markup=main_menu_kb())
        return

    if text not in {"да", "yes", "ok"}:
        await message.answer("Напиши <b>да</b> или <b>отмена</b>.")
        return

    data = await state.get_data()
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if not antifraud.allow_transaction(user, data["amount"]):
        await message.answer("🚨 Подозрительная операция")
        return

    await tx_repo.create(
        user_id=user.id,
        amount=data["amount"],
        category_id=data["category_id"],
        tx_type=data["tx_type"],
        comment=data["comment"],
    )

    gamification.apply_transaction(user, data["amount"], data["tx_type"])
    achievement_service.check(user)

    await state.clear()
    await message.answer("✅ Операция сохранена!", reply_markup=main_menu_kb())
