import asyncio
from bot.bot import dp, bot, test_db_connection


async def main():
  
    if bot is None or dp is None:
        print("⛔ Остановка: бот не инициализирован. Проверьте TELEGRAM_TOKEN.")
        return

 
    print("🔍 Проверка подключения к базе данных...")
    if not test_db_connection():
        print("⛔ Остановка: не удалось подключиться к PostgreSQL.")
        return

 
    from bot.handlers.start import router as start_router
    dp.include_router(start_router)

    print("🚀 Бот запущен. Ожидание сообщений...")


    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка при работе бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())