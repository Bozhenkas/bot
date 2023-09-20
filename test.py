import aiosqlite

from db_methods import get_transactions, reverse_refactor_category, transactions_to_list


async def main():
    tg_id = 294057781  # Замените на нужный tg_id
    transactions = transactions_to_list(get_transactions(tg_id))
    print(*transactions, sep='\n')


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
