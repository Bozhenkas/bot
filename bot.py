import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, choice, back, categories, transactions, total
from config import TOKEN


# Запуск бота
async def main():
    bot = Bot(token=TOKEN, parse_mode="MarkdownV2")
    dp = Dispatcher()

    dp.include_routers(start.router, choice.router, back.router, categories.router, transactions.router, total.router)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
