import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Вставь свой токен бота
TOKEN = "8166218766:AAHJ0unNRl02SbUUGJl0ipqQ9NM8O0Rxid0"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer("Привет! Я бот для расчёта калорий. Введи данные в формате: \n\n"
                         "`возраст вес рост пол активность`\n\n"
                         "Пример: `25 70 175 м 1.55`\n"
                         "Активность: 1.2 (минимум), 1.375 (лёгкая), 1.55 (средняя), 1.725 (высокая), 1.9 (очень высокая).", 
                         parse_mode="Markdown")

# Хэндлер для расчёта калорий
@dp.message_handler()
async def calculate_calories(message: Message):
    try:
        data = message.text.split()
        if len(data) != 5:
            raise ValueError
        
        age, weight, height, gender, activity = int(data[0]), float(data[1]), float(data[2]), data[3].lower(), float(data[4])

        if gender == "м":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == "ж":
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            raise ValueError

        total_calories = bmr * activity

        await message.answer(f"Твоя базовая норма калорий: {round(total_calories)} ккал/день")

    except ValueError:
        await message.answer("Ошибка! Проверь ввод. Пример: `25 70 175 м 1.55` (возраст, вес, рост, пол, активность).", parse_mode="Markdown")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
