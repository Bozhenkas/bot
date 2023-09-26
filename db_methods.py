import aiosqlite
import datetime
import pytz

from methods import format_datetime


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
            return await get_user_data(tg_id)  # возвращаем все данные пользователя
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
        rows = await cursor.fetchall()
        # Получаем все строки результата
        transactions = [list(row) for row in rows]

        # Возвращаем список транзакций
        return transactions


def refactor_category(category):
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


async def transactions_to_list(transactions) -> list:
    new_transactions = []
    for transaction in transactions:
        new_transactions.append(
            [transaction[0], reverse_refactor_category(transaction[2]), transaction[3],
             format_datetime(transaction[4])])
    new_transactions.reverse()
    return new_transactions


async def get_transaction_by_id(transaction_id: int) -> str:
    conn = await aiosqlite.connect('db.db')
    cursor = await conn.cursor()
    await cursor.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
    transaction_list = list(await cursor.fetchone())
    transaction_list[4] = format_datetime(transaction_list[4])
    transaction = (f'*\\{transaction_list[3]} ₽* \\| {reverse_refactor_category(transaction_list[2])} \\| '
                   f'{transaction_list[4]}')
    return transaction


async def delete_transaction_by_id(transaction_id: int) -> bool:
    async with aiosqlite.connect('db.db') as db:
        # Создание курсора
        async with db.cursor() as cursor:
            # Шаг 1: Находим транзакцию по id
            await cursor.execute("SELECT [tg id], category, summ FROM transactions WHERE id = ?", (transaction_id,))
            transaction_data = await cursor.fetchone()

            if transaction_data:
                tg_id, category, summ = transaction_data

                # Шаг 2: Вычитаем сумму из категории пользователя
                await cursor.execute(f"UPDATE users SET {category} = {category} - ? WHERE tg_id = ?", (summ, tg_id,))

                # Шаг 3: Вычитаем сумму из общей суммы пользователя
                await cursor.execute("UPDATE users SET summ = summ - ? WHERE tg_id = ?", (summ, tg_id,))

                # Шаг 4: Удаляем транзакцию из таблицы transactions
                await cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

                # Сохраняем изменения в базе данных
                await db.commit()
                return True
            else:
                print(f"Транзакция с id {transaction_id} не найдена")
                return False
