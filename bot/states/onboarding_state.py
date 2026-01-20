from aiogram.fsm.state import StatesGroup, State

class OnboardingState(StatesGroup):
    intro = State()
    features = State()
    fairness = State()      # приватность + антифрод
    gamification = State()  # XP, уровни, ачивки
