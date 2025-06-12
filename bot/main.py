import os
import json
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ContentType
from aiogram.utils.web_app import WebAppInfo # Для WebAppInfo

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем данные из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YOUR_TELEGRAM_ID = int(os.getenv('YOUR_TELEGRAM_ID')) # Преобразуем в int
MINI_APP_URL = os.getenv('MINI_APP_URL')

# Проверяем наличие всех необходимых переменных
if not TOKEN or not YOUR_TELEGRAM_ID or not MINI_APP_URL:
    print("Ошибка: Убедитесь, что все переменные (TELEGRAM_BOT_TOKEN, YOUR_TELEGRAM_ID, MINI_APP_URL) заданы в файле .env")
    exit()

# Инициализируем бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем клавиатуру с кнопкой для открытия Mini App
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Запустить ИИ-Таргетолога", web_app=WebAppInfo(url=MINI_APP_URL))]
    ])
    await message.answer("Привет! Я твой ИИ-таргетолог для Meta Ads. Нажми кнопку, чтобы начать настройку кампании:", reply_markup=keyboard)

# Обработчик данных, приходящих из Mini App
@dp.message(content_type=ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    # message.web_app_data.data содержит JSON-строку, отправленную из Mini App
    try:
        data = json.loads(message.web_app_data.data)

        # Извлекаем данные из Mini App
        request_type = data.get('type', 'unknown')
        product_name = data.get('product_name', 'Не указано')
        campaign_goal = data.get('campaign_goal', 'Не указана')
        target_audience_description = data.get('target_audience_description', 'Не указано')
        budget = data.get('budget', 'Не указан')
        timestamp = data.get('timestamp', 'N/A')

        # Пока просто отправляем тебе полученные данные.
        # Здесь будет логика вызова ИИ-модели для генерации рекомендаций.
        response_message = (
            f"📊 Получен запрос из Mini App:\n"
            f"Тип запроса: {request_type}\n"
            f"Продукт: {product_name}\n"
            f"Цель кампании: {campaign_goal}\n"
            f"Описание ЦА: {target_audience_description}\n"
            f"Бюджет: {budget} USD\n"
            f"Время запроса: {timestamp}\n\n"
            f"✨ (Здесь ИИ сгенерирует рекомендации по таргетингу, креативам, бюджету и улучшению.)"
        )

        # Отправляем тебе уведомление
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=response_message)
        await message.answer("Ваш запрос получен! ИИ-таргетолог обрабатывает данные и скоро пришлет рекомендации.")
        print(f"Получены и обработаны данные из Mini App: {data}")

    except json.JSONDecodeError:
        await message.answer("Ошибка при обработке данных из Mini App: Некорректный JSON.")
        print(f"Ошибка JSON при получении данных из Mini App: {message.web_app_data.data}")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке данных из Mini App.")
        print(f"Общая ошибка при обработке данных из Mini App: {e}, данные: {message.web_app_data.data}")


async def main():
    print("ИИ-Таргетолог Бот запущен. Ожидаю сообщений и данных из Mini App...")
    # Запускаем обработку входящих обновлений
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())