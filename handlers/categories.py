from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.for_choice import get_choice_kb
from handlers.txt import summ_text, complete_transaction_text, error_number_text

from db_methods import add_transactions_to_bd
from methods import is_number

router = Router()
available_categories = ['🍟 Mак', '🐔 KFC', '🍔 БК', '🍕🥦🥞 Другое']


class AddSumm(StatesGroup):
    choosing_summ = State()


@router.message(F.text.in_(available_categories))
async def msg_add_summ(message: types.Message, state: FSMContext):
    print('hui')
    await state.update_data(chosen_category=message.text)
    await message.answer(summ_text, reply_markup=None, input_field_placeholder='Введи сумму')
    await state.set_state(AddSumm.choosing_summ)  # ставим состояние ввода суммы


@router.message(AddSumm.choosing_summ)
async def msg_add_summ(message: types.Message, state: FSMContext):
    if is_number(message.text):
        category = await state.get_data()
        await add_transactions_to_bd(message.from_user.id, category['chosen_category'], float(message.text))
        await message.answer(complete_transaction_text, reply_markup=get_choice_kb())
        await state.clear()  # сбрасываем состояние
    else:
        await message.answer(error_number_text, input_field_placeholder='Введи сумму')
