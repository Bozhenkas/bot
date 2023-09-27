from aiogram import Router, F, types
from aiogram.filters.command import Command

from db_methods import add_to_db
from handlers.txt import start_text
from keyboards.for_choice import get_choice_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await add_to_db(message.from_user.id, message.from_user.username)
    await message.answer(start_text, reply_markup=get_choice_kb(), parse_mode="MarkdownV2")
