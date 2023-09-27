import datetime
import pytz

from aiogram import Router, types
from aiogram.filters.command import Command

from db_methods import get_total_summ
from methods import format_datetime

router = Router()
wl = [294057781]


@router.message(Command('total'))
async def cmd_total(message: types.Message):
    if message.from_user.id in wl:
        date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S %Z")[:-4]
        time = format_datetime(date)
        await message.answer(f'Общая сумма на {time}:\n'
                             f'*{await get_total_summ()} ₽*')
    else:
        await message.answer('Отказано в доступе 🤡')
        with open('pidors.txt', 'a') as f:
            string = ''
            string += str(message.from_user.id)
            string += ' '
            string += str(message.from_user.username)
            string += '\n'
            f.write(string)
