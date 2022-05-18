import datetime
import working_with_databases as DB


class Event:
    """
    Класс для обработки событий и соответсвующих им действий
    """

    def __init__(self, user_text):
        self.user_text = user_text

    def start(self):
        """
        Проверяет наличие команд и делает запись через сооотвествующий класс
        """

        match self.user_text:
            case str(text) if '/' in text:
                pass
            case str(text) if len(text.split()) == 2:
                setattr(self, 'value', text.split()[0])
                setattr(self, 'category', text.split()[1])

                SE = SingleExpenses(self.category, self.value)
                SE.write_single_expenses()


class Calculate:
    """
    Проведение подсчетов
    """

    def __init__(self):
        self.reader = DB.ReadFromTable()

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
        # self.date = '2022-05-28'  # (Данная строчка нужна кода нужна только при тестировании)
        self.category = category
        self.value = value

        self.last_expenses = DB.ReadFromTable().get_last_expenses()
        self.last_day_expenses = DB.ReadFromTable().get_last_month_expenses()

        self.write = DB.WriteToTable()
    
    def change_day(self):
        """
        Смена даты
        """

        DB.CreateLog().write_day_log()
        self.check_last_day_expenses()
        self.write.write_month_expenses(self.day_id, self.date, Calculate().sum_day_expenses(), '0', '0')
        DB.ClearTable().clear_day_expenses()
        self.expenses_id = '1'

    def change_month(self):
        """
        Смена месяца
        """

        DB.CreateLog().write_month_log()
        DB.ClearTable().clear_month_expenses()
        self.day_id = '1'

    def check_last_expenses(self):
        """
        Проверка на наличие предыдущей записи расходов в течение дня и присвоение id для текущей записи
        """

        if self.last_expenses:
            self.expenses_id = str(int(self.last_expenses[0]) + 1)

    def check_last_day_expenses(self):
        """
        Проверка на наличие предыдущей записи в таблице расходов за месяц и присвоение id для текущей записи
        """

        if self.last_day_expenses:
            self.day_id = str(int(self.last_day_expenses[0]) + 1)

    def check_day(self):
        """
        Проверка соответсвия текущей даты с датой последней записи в таблице расходов за день
        """

        if self.last_expenses:
            return self.date == self.last_expenses[1]
        return True

    def check_month(self):
        """
        Проверка соответсвия текущего месяца с месяцем последней записи в таблице расходов за месяц
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
        else:
            self.check_last_expenses()

        DB.WriteToTable().write_single_expenses(self.expenses_id, self.date, self.category, self.value)
