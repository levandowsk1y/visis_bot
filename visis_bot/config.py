from environs import Env
import os

print("🔧 Текущая директория:", os.getcwd())
print("📄 Файлы в папке:", os.listdir(os.getcwd()))

env = Env()
env.read_env()

print("✅ .env загружен (или попытка была)")

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
print("🔑 BOT_TOKEN загружен:", TELEGRAM_TOKEN[:10] + "...")
