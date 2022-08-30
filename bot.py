#!/usr/bin/env python3

# version 1.0

# author Ilya Temerev
# email kidmoto@yandex.ru

import core
import working_with_databases as DB
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def create_all_tables():
    """
    Создание всех таблиц в базе данных, если их еще не существует
    """

    DB.CreateTables().create_regular_income()
    DB.CreateTables().create_single_income()
    DB.CreateTables().create_regular_expenses()
    DB.CreateTables().create_day_expenses()
    DB.CreateTables().create_month_expenses()


@dp.message_handler(commands=['start', 'help'])
async def help(message: types.Message):
    await message.answer('''
Данные вводятся в поле ввода сообщения в следующем виде <сумма> <категория> (без треугольных скобок) через пробел, при этом <категория> обязательно должна являться одним словом.

Примеры:
Для внесения записи в таблицу текущих расходов необходимо ввести в поле ввода текстового сообщения телеграмма следующую запись:
300 такси
Затем нажать кнопку откправки сообщения в чат.

Если необходимо внести запись после команды, например для внесения записи в таблицу регулярных доходов, необходимо ввести в поле ввода текстового сообщения телеграмма следующую запись:
/RI 50000 Зарплата
Затем нажать кнопку откправки сообщения в чат.

Все команды, позволябщие работать с программой:

Добавить запись в таблицу Регулярных Доходов: /RI <сумма> <категория>
Посмотреть все записи из таблицы Регулярных Доходов: /readRI
Удалить запись из таблицы Регулярных Доходов: /delRI <категория>

Добавить запись в таблицу Регулярных Расходов: /RI <сумма> <категория>
Посмотреть все записи из таблицы Регулярных Расходов: /readRI
Удалить запись из таблицы Регулярных Расходов: /delRI <категория>

Добавить запись в таблицу Разовых Доходов: /RI <сумма> <категория>
Посмотреть все записи из таблицы Разовых Доходов: /readRI
Удалить запись из таблицы Разовых Доходов: /delRI <категория>

Добавить запись в таблицу Текущих (разовых) расходов: <сумма> <категория>
Посмотреть все записи из таблицы Расходов за день: /readDAY
Посмотреть все записи из таблицы Расходов за месяц: /readMON
Удалить запись из таблицы Расходов за день: /delDAY <id>
''')


@dp.message_handler()
async def echo(message: types.Message):
    """
    Обработка сообщения через ядро (core.py) и ответ на сообщение
    """

    one_event = core.Event(message.text)
    one_event.start()

    await message.answer(one_event.answer)


if __name__ == '__main__':
    create_all_tables()
    executor.start_polling(dp)
