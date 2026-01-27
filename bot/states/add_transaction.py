from aiogram.fsm.state import State, StatesGroup


class AddTransactionState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()
    waiting_for_comment = State()
    waiting_for_confirm = State()
