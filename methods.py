import datetime


def format_datetime(input_datetime_str) -> str:
    # Словарь для преобразования номера месяца в его название
    month_names = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'sep',
        10: 'oct.',
        11: 'nov.',
        12: 'dec.'
    }

    # Преобразуем строку с датой и временем в объект datetime
    input_datetime = datetime.datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

    # Извлекаем день, месяц и время
    day = input_datetime.day
    month = input_datetime.month
    time = input_datetime.strftime('%H:%M')

    # Форматируем дату и месяц
    formatted_date = f"{day} {month_names[month]}"

    # Возвращаем окончательную строку
    formatted_datetime = f"{formatted_date} в {time}"
    return formatted_datetime


def is_number(value):
    try:
        float(value)  # Попробуйте преобразовать в число
        return True
    except ValueError:
        return False


async def transaction_to_inline(transactions) -> list:
    inline_buttons_list = []
    for transaction in transactions:
        inline_buttons_list.append(
            f' {transaction[2]} ₽ |'
            f' {transaction[1]} |'
            f' {transaction[3]}')
    return inline_buttons_list
