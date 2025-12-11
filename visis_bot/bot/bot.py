import os
from pathlib import Path
from aiogram import Bot, Dispatcher
from openai import OpenAI
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / ".env"

print(f"🔧 Путь к .env: {ENV_PATH}")
if ENV_PATH.exists():
    print("✅ Файл .env найден")
    load_dotenv(dotenv_path=ENV_PATH)
else:
    print("❌ Файл .env не найден — используем переменные из окружения")


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    print("❌ ОШИБКА: TELEGRAM_TOKEN не найден в .env или системе")
else:
    print(f"✅ TELEGRAM_TOKEN загружен: {TELEGRAM_TOKEN[:10]}...")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    print("✅ OPENAI_API_KEY загружен")
else:
    print("❌ OPENAI_API_KEY не найден в .env")


DB_CONFIG = {
    "host": "localhost",
    "database": "visisdb",
    "user": "zikres",
    "password": "123"
}


def test_db_connection():
    """Проверка подключения к PostgreSQL"""
    try:
        import psycopg2
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        conn.close()
        print("✅ Подключение к базе данных PostgreSQL установлено")
        return True
    except Exception as e:
        print(f"❌ Не удалось подключиться к базе данных: {e}")
        return False



if TELEGRAM_TOKEN:
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        dp = Dispatcher()
        print("✅ Bot и Dispatcher инициализированы")
    except Exception as e:
        print(f"❌ Ошибка инициализации бота: {e}")
        bot = None
        dp = None
else:
    print("🚫 Bot не создан: нет токена")
    bot = None
    dp = None


if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI клиент создан")
    except Exception as e:
        print(f"❌ Ошибка инициализации OpenAI: {e}")
        openai_client = None
else:
    openai_client = None
    print("🚫 OpenAI клиент не создан: нет ключа")