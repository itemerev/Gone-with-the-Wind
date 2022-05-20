import core
import working_with_databases as DB

from config import TOKEN

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def create_all_tables():
    DB.CreateTables().create_regular_income()
    DB.CreateTables().create_single_income()
    DB.CreateTables().create_regular_expenses()
    DB.CreateTables().create_day_expenses()
    DB.CreateTables().create_month_expenses()

@dp.message_handler()
async def echo(message: types.Message):
    one_event = core.Event(message.text)
    one_event.start()
    
    sum_per_day = core.Calculate().sum_day_expenses()

    await message.answer(f'Total spent per day {sum_per_day} rubles')


if __name__ == '__main__':
    create_all_tables()
    executor.start_polling(dp)

