from aiogram import Router, F, types

from handlers.txt import menu_text
from keyboards.for_choice import get_choice_kb

router = Router()


@router.message(F.text == '⬅️ Назад')
async def msg_go_back(message: types.Message):
    await message.answer(menu_text, reply_markup=get_choice_kb())
