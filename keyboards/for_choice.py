from aiogram import types


# жёстко отдельный файл для создания трёх кнопок...

def get_choice_kb():
    k = [
        [types.KeyboardButton(text='💵 Добавить сумму'), types.KeyboardButton(text='🧾 Транзакции')],
        [types.KeyboardButton(text='ℹ️ Информация')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=k,
        resize_keyboard=True,
        input_field_placeholder="Нажми на кнопочку",
        one_time_keyboard=True
    )
    return keyboard
