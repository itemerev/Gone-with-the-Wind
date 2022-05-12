import datetime
import working_with_databases as db


class ParseInput:
    """
    Распознавание введенного текста
    """

    def __init__(self, input_text):
        self.input_text = input_text

        self.expenses_data = None
        self.value = None
        self.category = None

    def check_exit(self):
        """
        Проверка команды завершения работы приложения
        """

        return self.input_text == 'exit'

    def check_command(self):
        """
        Проверка поступающего от пользовтеля текста на наличие команд
        """

        return '/' in self.input_text

    def parse_single_expenses(self):
        """
        Разделение поступающего от пользовтеля текста на категорию затрат и сумму затрат
        """

        self.expenses_data = self.input_text.split()  # TODO: строка может содержать отличное от 2-х число слов
        self.value = self.expenses_data[0]
        self.category = self.expenses_data[1]


class Calculate:
    """
    Проведение подсчетов
    """

    def __init__(self):
        self.expenses = [int(row[-1][-1]) for row in db.ReadFromTable.all_line]

    def sum_day_expenses(self):
        """
        Сумма всех расходов в течение дня
        """

        return sum(self.expenses)


class RegularIncome:
    pass


class SingleIncome:
    pass


class RegularExpenses:
    pass


class SingleExpenses:
    """
    Класс для внесения записи разовых расходов и определения таблицы для внесения записи
    """

    expenses_id = '1'
    day_id = '1'

    def __init__(self, category, value):
        # self.date = str(datetime.date.today())
        self.date = '2022-05-13'
        self.category = category
        self.value = value

        self.last_expenses = db.ReadFromTable().get_last_expenses()
        self.last_day_expenses = db.ReadFromTable().get_last_month_expenses()

        self.write = db.WriteToTable()

    # TODO: Исправить работоспособность следующих 4-х методов класса
    def check_last_expenses(self):
        """
        Проверка на наличие предыдущей записи расходов в течение дня и присвоение id для текущей записи
        """

        if self.last_expenses:
            self.expenses_id = str(int(self.last_expenses[0]) + 1)

    def check_last_day_expenses(self):
        """
        Проверка на наличие предыдущей записи расходов за день и присвоение id для текущей записи
        """

        if self.last_day_expenses:
            self.day_id = str(int(self.last_day_expanses[0]) + 1)

    def check_month(self):
        """
        Проверка соответсвия текущего месяца с месяцем последней записи в таблице рачходов за месяц
        """

        last_month = self.last_expenses[1][5:7]
        return self.date[5:7] == last_month

    def write_single_expenses(self):
        """
        Сохранение данных о разовых расходах в БД
        """

        if not self.last_expenses or self.date == self.last_expenses[1]:
            self.write.write_single_expenses(self.date, self.category, self.value)
        elif check_month():
            expenses_per_day = Calculate.sum_day_expenses()
            self.write.write_month_expenses(self.last_expenses[1], expenses_per_day, budget_per_day=0, balance=0)
            db.CreateLog().write_day_log()
            db.ClearTable().clear_day_expenses()
            self.write.write_single_expenses(self.date, self.category, self.value)
