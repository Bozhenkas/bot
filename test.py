import aiosqlite

from db_methods import get_transactions, reverse_refactor_category, transactions_to_list, get_transaction_by_id


async def main():
    print(await get_transaction_by_id(373))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
