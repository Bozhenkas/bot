import aiosqlite
import datetime
import pytz


# проверка есть ли в базе - есть (совмещено со вторым)
# добавление в базу нового челепиздрика - есть
# добавление транзакции
# получение данных о транзакциях человека по его айди


async def add_to_db(tg_id, tg_nick=None) -> bool:
    # Подключаемся к базе данных (или создаем ее, если она не существует)
    async with aiosqlite.connect('db.db') as conn:
        cursor = await conn.cursor()

        # SQL-запрос для добавления новой записи
        insert_query = """
        INSERT INTO users (tg_id, tg_nick)
        VALUES (?, ?)
        """

        try:
            await cursor.execute(insert_query, (tg_id, tg_nick))
            await conn.commit()
            return True  # возвращаем True, если добавили
        except aiosqlite.IntegrityError:
            await conn.commit()
            return False  # возвращаем False, если уже есть


async def add_transactions_to_bd(tg_id, category, summ) -> bool:
    async with aiosqlite.connect('db.db') as conn:
        date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S %Z")[:-4]
        cursor = await conn.cursor()

        # SQL-запрос для добавления новой записи
        insert_query = """
        INSERT INTO transactions ([tg id], category, summ, date)
        VALUES (?, ?, ?, ?)
        """

        try:
            await cursor.execute(insert_query, (tg_id, refactor_category(category), summ, date))

            await conn.commit()
            await update_user_summ(tg_id, refactor_category(category), summ)
            return True  # если всё четко
        except aiosqlite.IntegrityError as e:
            await conn.commit()
            return False  # если не удалось


async def update_user_summ(tg_id, category, summ) -> ():
    async with aiosqlite.connect('db.db') as conn:
        cursor = await conn.cursor()

        # SQL-запрос для обновления записи
        update_query = f"""
        UPDATE users
        SET {category} = {category} + ?,
            summ = summ + ?
        WHERE tg_id = ?
        """

        try:
            await cursor.execute(update_query, (summ, summ, tg_id))
            await conn.commit()
            return get_user_data(tg_id)  # возвращаем все данные пользователя
        except aiosqlite.IntegrityError as e:
            print(f"Ошибка при обновлении данных: {e}")


async def get_user_data(tg_id):
    async with aiosqlite.connect('db.db') as conn:
        cursor = await conn.cursor()

        # SQL-запрос для выборки данных по tg_id
        select_query = """
        SELECT * FROM users
        WHERE tg_id = ?
        """

        try:
            await cursor.execute(select_query, (tg_id,))
            user_data = await cursor.fetchone()  # Получаем одну строку с данными пользователя
            return user_data  # Возвращаем данные пользователя или None, если не найдено
        except aiosqlite.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None


async def get_transactions(tg_id) -> list:
    # Открываем соединение с базой данных
    async with aiosqlite.connect('db.db') as db:
        # Создаем курсор
        cursor = await db.cursor()

        # Выполняем SQL-запрос для выборки всех транзакций для данного tg_id
        await cursor.execute('SELECT * FROM transactions WHERE [tg id] = ?', (tg_id,))

        # Получаем все строки результата
        transactions = list(await cursor.fetchall())

        # Возвращаем список транзакций
        return transactions


def refactor_category(category):
    print(category)
    if category == '🍟 Mак':
        return 'vit'
    elif category == '🐔 KFC':
        return 'kfc'
    elif category == '🍔 БК':
        return 'bk'
    elif category == '🍕🥦🥞 Другое':
        return 'other'
    else:
        raise ValueError("Недопустимая категория")


def reverse_refactor_category(category):
    print(category)
    if category == 'vit':
        return '🍟 Mак'
    elif category == 'kfc':
        return '🐔 KFC'
    elif category == 'bk':
        return '🍔 БК'
    elif category == 'other':
        return '🍕🥦🥞 Другое'
    else:
        raise ValueError("Недопустимая категория")


def transactions_to_list(transactions):
    new_transaction = ''
    for transaction in transactions:
        new_transaction += transaction[:2]
        new_transaction += reverse_refactor_category(transaction[2])
        new_transaction += transaction[2:]
        new_transaction += '\n'
    return new_transaction


def is_number(value):
    try:
        float(value)  # Попробуйте преобразовать в число
        return True
    except ValueError:
        return False
