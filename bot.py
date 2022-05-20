import core
import working_with_databases as DB
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def create_all_tables():
    """
    Создание всех таблице в базе данных, если их не существует
    """

    DB.CreateTables().create_regular_income()
    DB.CreateTables().create_single_income()
    DB.CreateTables().create_regular_expenses()
    DB.CreateTables().create_day_expenses()
    DB.CreateTables().create_month_expenses()

@dp.message_handler()
async def echo(message: types.Message):
    """
    Обработка сообщения через ядро (core.py) и ответ на него
    """

    one_event = core.Event(message.text)
    one_event.start()

    await message.answer(one_event.answer)


if __name__ == '__main__':
    create_all_tables()
    executor.start_polling(dp)
