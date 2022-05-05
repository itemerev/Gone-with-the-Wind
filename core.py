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


class RegularIncome:
    pass


class SingleIncome:
    pass


class RegularExpenses:
    pass


class SingleExpenses:
    expenses_id = '1'

    def __init__(self, category, value):
        db.create_day_expenses()

        self.date = datetime.date.today()
        self.category = category
        self.value = value

        self.last_expenses = db.ReadFromTable.get_last_expenses()

    def check_last_expenses(self):
        """
        Проверка на наличие предыдущей записи и присвоение id для текущей записи
        """

        if not self.last_expenses:
            self.expenses_id = '1'
        else:
            self.expenses_id = str(int(self.last_expenses[0]) + 1)

    def write_single_expenses(self):
        """
        Сохранение данных о разовых расходах в БД
        """

        # Добавить условие, если дата внесения записи изменилась
        db.WriteToTable.write_single_expenses(self.expenses_id, self.date, self.category, self.value)
        self.expenses_id += 1
