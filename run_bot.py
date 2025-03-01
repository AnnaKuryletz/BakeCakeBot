import asyncio
from aiogram import Bot, Dispatcher
import  os
import django
import sys


TOKEN = "7996830180:AAG7WWT5MOKU8s40MfCxrAKMeYyulVh-BPM"
# Определяем путь к корню проекта (BakeCakeBot)


# Получаем абсолютный путь к папке, где находится run_bot.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к backend
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# Путь к bake_cake
BAKE_CAKE_DIR = os.path.join(BACKEND_DIR, "bake_cake")

# Добавляем backend в sys.path
sys.path.append(BACKEND_DIR)
sys.path.append(BAKE_CAKE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bake_cake.settings")


# Инициализируем Django
django.setup()

from staticfiles.handlers import router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем роутер с обработчиками
    dp.include_router(router)

    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


