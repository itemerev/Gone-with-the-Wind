from config import TOKEN

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)

