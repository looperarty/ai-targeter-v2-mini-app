import os
import json
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F # <-- ИЗМЕНЕНИЕ 1: Добавили 'F' сюда
from aiogram.filters import CommandStart
from aiogram.enums import ContentType
from aiogram.types import WebAppInfo

# Импорт для работы с Google Gemini API
import google.generativeai as genai

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем данные из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YOUR_TELEGRAM_ID = int(os.getenv('YOUR_TELEGRAM_ID'))
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
MINI_APP_URL = os.getenv('MINI_APP_URL')

# Проверяем наличие всех необходимых переменных
if not TOKEN or not YOUR_TELEGRAM_ID or not GOOGLE_GEMINI_API_KEY or not MINI_APP_URL:
    print("Ошибка: Убедитесь, что все переменные (TELEGRAM_BOT_TOKEN, YOUR_TELEGRAM_ID, GOOGLE_GEMINI_API_KEY, MINI_APP_URL) заданы в файле .env")
    exit()

# Конфигурируем Google Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
# Выбираем модель Gemini, которую будем использовать
model = genai.GenerativeModel('gemini-pro')


# Инициализируем бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Запустить ИИ-Таргетолога", web_app=WebAppInfo(url=MINI_APP_URL))]
    ])
    await message.answer("Привет! Я твой ИИ-таргетолог для Meta Ads. Нажми кнопку, чтобы начать настройку кампании:", reply_markup=keyboard)


# Обработчик данных, приходящих из Mini App
@dp.message(F.web_app_data) # <-- ИЗМЕНЕНИЕ 2: Используем F.web_app_data для фильтрации
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)

        # Извлекаем данные из Mini App
        request_type = data.get('type', 'campaign_analysis')
        product_name = data.get('product_name', 'не указан')
        campaign_goal = data.get('campaign_goal', 'не указана')
        target_audience_description = data.get('target_audience_description', 'не указано')
        budget = data.get('budget', 'не указан')

        user_input = (
            f"Мой продукт/услуга: {product_name}. "
            f"Моя цель кампании в Meta Ads: {campaign_goal}. "
            f"Предполагаемая целевая аудитория: {target_audience_description}. "
            f"Планируемый бюджет: {budget} USD.\n\n"
            "Сгенерируй детальные рекомендации для настройки рекламной кампании в Meta Ads (Facebook/Instagram), "
            "включая:\n"
            "1. Рекомендации по целевой аудитории (демография, интересы, поведение) с конкретными примерами.\n"
            "2. 3-5 вариантов рекламных текстов/заголовков для разных плейсментов Meta Ads.\n"
            "3. Идеи для визуальных креативов.\n"
            "4. Рекомендации по оптимизации бюджета и ставок.\n"
            "Отвечай на русском языке."
        )

        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text="⚙️ ИИ-таргетолог обрабатывает ваш запрос. Это может занять до минуты...")
        await message.answer("Запрос отправлен ИИ-модели. Ожидайте рекомендации в личных сообщениях.")

        # Отправляем запрос к Gemini API
        response = await model.generate_content_async(user_input)

        # Формируем сообщение с результатом от ИИ
        gemini_response_text = response.text if response.text else "ИИ не смог сгенерировать ответ. Попробуйте еще раз или измените запрос."

        final_message = (
            f"✨ **Рекомендации ИИ-таргетолога для Meta Ads:**\n\n"
            f"{gemini_response_text}\n\n"
            f"--- \nВаш запрос был:\nПродукт: {product_name}\nЦель: {campaign_goal}\n"
            f"Описание ЦА: {target_audience_description}\nБюджет: {budget} USD"
        )

        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=final_message, parse_mode='Markdown')
        print(f"Получены и обработаны данные из Mini App, отправлены рекомендации: {data}")

    except json.JSONDecodeError:
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text="🚫 Ошибка: Некорректный формат данных из Mini App.")
        await message.answer("Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова.")
        print(f"Ошибка JSON при получении данных из Mini App: {message.web_app_data.data}")
    except Exception as e:
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=f"🚫 Произошла ошибка при обращении к ИИ: {e}")
        await message.answer("Произошла ошибка при получении рекомендаций от ИИ. Попробуйте позже.")
        print(f"Общая ошибка при обработке данных из Mini App или вызове ИИ: {e}, данные: {message.web_app_data.data}")


async def main():
    print("ИИ-Таргетолог Бот запущен. Ожидаю сообщений и данных из Mini App...")
    # Запускаем обработку входящих обновлений
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())