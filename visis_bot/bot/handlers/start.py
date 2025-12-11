from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import psycopg2
from bot.bot import DB_CONFIG, openai_client, test_db_connection
from ..prompt import SCHEMA_PROMPT

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я могу ответить на вопросы о видео.\n"
        "Например:\n"
        "• Сколько всего видео?\n"
        "• На сколько выросли просмотры 28 ноября 2025?"
    )


def get_sql_query_from_llm(question: str) -> str:
    """
    Отправляет вопрос в OpenAI и получает SQL
    """
    if not openai_client:
        print("❌ OpenAI клиент не инициализирован")
        return None

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SCHEMA_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.0,
            n=1
        )
        sql = response.choices[0].message.content.strip()

        if sql.startswith("```sql"):
            sql = sql[7:-3].strip()
        elif sql.startswith("```"):
            sql = sql[3:-3].strip()

        return sql
    except Exception as e:
        print(f"❌ Ошибка при обращении к OpenAI: {e}")
        return None


def execute_sql_query(sql: str) -> int:
    """
    Выполняет SQL и возвращает одно число
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        value = result[0] if result and result[0] is not None else 0
        print(f"📊 Результат из БД: {value}")
        return value
    except Exception as e:
        print(f"❌ Ошибка выполнения SQL: {e}")
        return 0


@router.message(F.text)
async def handle_question(message: Message):
    question = message.text.strip()
    if not question:
        return

    print(f"📝 Вопрос пользователя: {question}")


    if not test_db_connection():
        await message.answer("❌ База данных недоступна.")
        return


    if not openai_client:
        await message.answer("🔧 OpenAI не настроен — проверьте API-ключ.")
        return

    sql = get_sql_query_from_llm(question)
    if not sql:
        await message.answer("❌ Не удалось сгенерировать SQL-запрос. Проверьте подключение к OpenAI.")
        return

    print(f"🔧 Сгенерирован SQL: {sql}")

    result = execute_sql_query(sql)
    await message.answer(str(result))