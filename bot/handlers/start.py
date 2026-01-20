from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.repositories.user_repo import UserRepository
from core.services.onboarding_service import OnboardingService
from bot.states.onboarding_state import OnboardingState
from bot.keyboards.onboarding import onboarding_next_kb
from bot.keyboards.main_menu import main_menu_kb
from bot.ui.main_menu_screen import render_main_screen


router = Router()

user_repo = UserRepository()
onboarding_service = OnboardingService()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    # 1️⃣ Загружаем/создаём пользователя
    user = await user_repo.create_if_not_exists(message.from_user.id)

    # 2️⃣ Проверяем, нужен ли онбординг
    if await onboarding_service.needs_onboarding(user):
        await state.set_state(OnboardingState.intro)

        await message.answer(
            text=(
                "Привет! 👋\n\n"
                "Я помогу тебе отслеживать доходы и расходы, "
                "прокачивать финансовую дисциплину и строить планы 📊💡\n\n"
                "Давай быстро расскажу, как всё устроено. Это займёт меньше минуты 😉"
            ),
            reply_markup=onboarding_next_kb(),
        )
        return


    await render_main_screen(message, user)

