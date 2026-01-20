from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.onboarding_state import OnboardingState
from bot.keyboards.onboarding import onboarding_next_kb, onboarding_finish_kb
from bot.keyboards import main_menu_kb
from infrastructure.repositories.user_repo import UserRepository
from core.services.onboarding_service import OnboardingService

router = Router()

user_repo = UserRepository()
onboarding = OnboardingService()


def _is_skip(message: Message) -> bool:
    return message.text and message.text.lower().startswith("пропустить")


@router.message(OnboardingState.intro)
async def onboarding_intro(message: Message, state: FSMContext):
    if _is_skip(message):
        await finish_onboarding(message, state)
        return

    await state.set_state(OnboardingState.features)
    await message.answer(
        text=(
            "📘 Кратко о возможностях:\n\n"
            "• Добавлять доходы и расходы в пару нажатий 💸\n"
            "• Смотреть статистику по дням, неделям и категориям 📊\n"
            "• Получать XP, уровни и ачивки за финансовую дисциплину 🏅\n"
            "• В будущем — планы, привычки и личный ежедневник 🗓\n\n"
            "Нажми «Дальше ▶️», чтобы узнать про конфиденциальность и честную игру."
        ),
        reply_markup=onboarding_next_kb(),
    )


@router.message(OnboardingState.features)
async def onboarding_fairness(message: Message, state: FSMContext):
    if _is_skip(message):
        await finish_onboarding(message, state)
        return

    await state.set_state(OnboardingState.fairness)
    await message.answer(
        text=(
            "🛡 Конфиденциальность и честная игра:\n\n"
            "• Твои реальные данные и суммы трат не попадут в рейтинги.\n"
            "• В лидербордах будут использоваться анонимные никнеймы (без @username).\n"
            "• Встроенная антифрод-система защищает от накруток XP и ачивок.\n"
            "• Рейтинги отражают только реальную активность — конкуренция здоровая 💚\n\n"
            "Дальше — немного про геймификацию."
        ),
        reply_markup=onboarding_next_kb(),
    )


@router.message(OnboardingState.fairness)
async def onboarding_gamification(message: Message, state: FSMContext):
    if _is_skip(message):
        await finish_onboarding(message, state)
        return

    await state.set_state(OnboardingState.gamification)
    await message.answer(
        text=(
            "🎮 Геймификация:\n\n"
            "• За действия (учёт расходов/доходов, выполнение планов) ты получаешь XP.\n"
            "• XP повышает твой уровень.\n"
            "• За особые достижения открываются ачивки.\n"
            "• В будущем появятся лидерборды и сезонные челленджи.\n\n"
            "Это помогает не просто считать деньги, а превращать дисциплину в игру 😊\n\n"
            "Нажми «Завершить ✅», чтобы закончить онбординг и получить первую награду."
        ),
        reply_markup=onboarding_finish_kb(),
    )


@router.message(OnboardingState.gamification)
async def onboarding_finish(message: Message, state: FSMContext):
    if _is_skip(message):
        await finish_onboarding(message, state)
        return

    await finish_onboarding(message, state)


async def finish_onboarding(message: Message, state: FSMContext):
    await state.clear()

    user = await user_repo.get_by_telegram_id(message.from_user.id)
    if user is None:
        user = await user_repo.create_if_not_exists(message.from_user.id)

    result = await onboarding.complete_onboarding(user)

    level = result["level"]
    total_xp = result["total_xp"]
    achievement = result["achievement"]
    earned_xp = result["xp"]

    text = (
        "🎉 <b>Онбординг завершён!</b>\n\n"
        f"✨ Вы получили: <b>+{earned_xp} XP</b>\n"
        f"🏅 Ваш уровень: <b>{level}</b>\n"
    )

    if achievement:
        text += (
            "\n🔥 <b>Новая ачивка!</b>\n"
            f"🏆 {achievement.name}\n"
            f"📝 {achievement.description}\n"
        )

    await message.answer(text, reply_markup=main_menu_kb())
