import core
import working_with_databases as DB

from config import TOKEN

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    one_event = core.Event(message.text)
    one_event.start()


    await message.answer('Data has added')


if __name__ == '__main__':
    executor.start_polling(dp)
