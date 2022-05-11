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

    def check_command(self):
        """
        Проверка поступающего от пользовтеля текста на наличие команд
        """

        return '/' in self.input_text

    def parse_single_expense(self):
        """
        Разделение поступающего от пользовтеля текста на категорию затрат и сумму затрат
        """

        self.expenses_data = entry_data.split()
        self.value = self.expenses_data[0]
        self.category = self.expenses_data[1]


class Calculate:
    def calc_day_expenses(self):
        expenses = [int(row[-1][-1]) for row in db.ReadFromTable.all_line
        return sum(expenses)


class RegularIncome:
    pass


class SingleIncome:
    pass


class RegularExpenses:
    pass


class SingleExpenses:
    expenses_id = '1'
    day_id = '1'

    def __init__(self, category, value):
        db.create_day_expenses()

        self.date = str(datetime.date.today())
        self.category = category
        self.value = value

        self.last_expenses = db.ReadFromTable.get_last_expenses()
        self.last_day_expenses = db.ReadFromTable.get_last_day_expenses()

    def check_last_expenses(self):
        """
        Проверка на наличие предыдущей записи и присвоение id для текущей записи
        """

        if self.last_expenses:
            self.expenses_id = str(int(self.last_expenses[0]) + 1)

    def check_last_day_expenses(self):
        if self.last_day_expenses:
            self.day_id = str(int(self.last_day_expanses[0]) + 1)

    def check_month():
        last_month = self.last_expenses[1][5:7]
        return self.date[5:7] == self.last_month

    def write_single_expenses(self):
        """
        Сохранение данных о разовых расходах в БД
        """

        # Добавить условие, если дата внесения записи изменилась
        if self.date == self.last_expenses[1]:
            db.WriteToTable.write_single_expenses(self.expenses_id, self.date, self.category, self.value)
        elif check_month():
            expenses_per_day = Calculate.calc_day_expenses()
            db.WriteToTable.write_month_expenses(self.day_id, self.last_expenses[1], expenses_per_day, budget_per_day=0, balance=0)
            db.CreateLog.write_day_log()
            db.ClearTable.clear_day_expenses()
            db.WriteToTable.write_single_expenses(self.expenses_id, self.date, self.category, self.value)
