from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboards.for_back import get_back_kb
from keyboards.for_categories import get_categories_kb
from handlers.txt import start_text, categories_text, information_text

from db_methods import get_user_data, get_transactions

router = Router()


@router.message(F.text == '💵 Добавить сумму')
async def msg_add_summ(message: types.Message, state: FSMContext):
    await message.answer(categories_text, reply_markup=get_categories_kb())


@router.message(F.text == 'ℹ️ Информация')
async def msg_information(message: types.Message):
    # вот тут должен быть код для
    await message.answer(information_text, reply_markup=get_back_kb())
