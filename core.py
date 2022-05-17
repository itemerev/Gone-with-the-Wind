import datetime
import working_with_databases as db


class Event:
    def __init__(self, user_text):
        self.parser = ParseInput(user_text)

    def start(self):
        if self.parser.check_command():
            pass
        elif self.parser.check_lenght():
            pass
        else:
            self.parser.parse_single_expenses()
            SE = SingleExpenses(self.parser.category, self.parser.value)
            SE.write_single_expenses()


class ParseInput:
    """
    Распознавание введенного текста
    """

    def __init__(self, text_to_process):
        self.text_to_process = itext_to_process

        self.split_text = self.text_to_process.split()

    def check_exit(self):
        return self.text_to_process == 'exit'

    def check_command(self):
        """
        Проверка поступающего от пользовтеля текста на наличие команд
        """

        return '/' in self.text_to_process

    def check_lenght():
        return len(self.split_text) == 2

    def parse_single_expenses(self):
        """
        Разделение поступающего от пользовтеля текста на категорию затрат и сумму затрат
        """

        setattr(self, 'value', self.split_text[0])
        setattr(self, 'category', self.split_text[1])


class Calculate:
    """
    Проведение подсчетов
    """

    def __init__(self):
        self.reader = db.ReadFromTable()

    def sum_day_expenses(self):
        """
        Сумма всех расходов в течение дня
        """

        self.reader.read_day_expenses()
        expenses_list = [int(row[-1]) for row in self.reader.all_line]
        return str(sum(expenses_list))


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
        self.date = str(datetime.date.today())
        # self.date = '2022-05-28'
        self.category = category
        self.value = value

        self.last_expenses = db.ReadFromTable().get_last_expenses()
        self.last_day_expenses = db.ReadFromTable().get_last_month_expenses()

        self.write = db.WriteToTable()
    
    def change_day(self):
        db.CreateLog().write_day_log()
        self.check_last_day_expenses()
        self.write.write_month_expenses(self.day_id, self.date, Calculate().sum_day_expenses(), '0', '0')
        db.ClearTable().clear_day_expenses()
        self.expenses_id = '1'

    def change_month(self):
        db.CreateLog().write_month_log()
        db.ClearTable().clear_month_expenses()
        self.day_id = '1'

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
            self.day_id = str(int(self.last_day_expenses[0]) + 1)

    def check_day(self):
        if self.last_expenses:
            return self.date == self.last_expenses[1]
        return True

    def check_month(self):
        """
        Проверка соответсвия текущего месяца с месяцем последней записи в таблице рачходов за месяц
        """
        
        if self.last_expenses:
            last_month = self.last_expenses[1][:7]
            return self.date[:7] == last_month
        return True

    def write_single_expenses(self):
        """
        Сохранение данных о разовых расходах в БД
        """
    
        if not self.check_month():
            self.change_day()
            self.change_month()
        elif not self.check_day():
            self.change_day()
            # self.day_id = str(int(self.day_id) + 1)
        else:
            self.check_last_expenses()

        db.WriteToTable().write_single_expenses(self.expenses_id, self.date, self.category, self.value)
