import datetime
import calendar
import working_with_databases as DB


class Event:
    """
    Класс для обработки событий и соответсвующих им действий
    """

    def __init__(self, user_text):
        self.text = user_text.split()
        self.answer = 'None'

    def start(self):
        """
        Проверяет наличие команд в вденном тексте
        """
        
        if '/' in self.text[0]:
            """
            При наличии команды, выполняет соотвествующую ей функцию
            """

            match self.text[0]:
                case '/RI':
                    setattr(self, 'value', self.text[1])
                    setattr(self, 'category', self.text[2])
                    ri = RegularIncome()
                    ri.add_regular_income(self.value, self.category)
                    self.answer = f'Даблен регулярный доход "{self.category}" в количестве {self.value} рублей'
                case '/readRI':
                    regular_income = DB.ReadFromTable().read_regular_income()
                    text = ''
                    for line in regular_income:
                        text += str(line).strip('(').strip(')') + '\n'
                    self.answer = text
                case '/delRI':
                    category = self.text[1]
                    DB.DeleteFromTable().delete_regular_income(category)

                    self.answer = f'Регулярный доход "{category}" удален'

        elif len(self.text) == 2:
            """
            При отсутствии команды делает запись в разовые расходы
            """

            setattr(self, 'value', self.text[0])
            setattr(self, 'category', self.text[1])

            SE = SingleExpenses(self.category, self.value)
            SE.write_single_expenses()

            self.answer = f'Бюджет на день {Calculate().budget()} рублей\nРасходов за сегодня {Calculate().sum_day_expenses()} рублей\nЖелательно потратить не больше чем {Calculate().balance()} рублей'


class Calculate:
    """
    Проведение подсчетов
    """

    def __init__(self):
        self.reader = DB.ReadFromTable()
        self.days = calendar.monthrange(int(str(datetime.date.today())[:4]), int(str(datetime.date.today())[5:7]))[1]

    def sum_day_expenses(self):
        """
        Сумма всех расходов в течение дня
        """

        self.reader.read_day_expenses()
        expenses_list = [int(row[-1]) for row in self.reader.all_line]
        return str(sum(expenses_list))

    def budget(self):
        """
        (Регулярные доходы + разовые доходы - регулярные расходы) и все это делить на количество дней в месяце
        """

        return str(round((int(RegularIncome().sum_regular_income) + int(SingleIncome().sum_single_income) - int(RegularExpenses().sum_regular_expenses)) / int(self.days)))

    def balance(self):
        return int(self.budget()) - int(self.sum_day_expenses())


class RegularIncome:
    """
    Работа с данными регулярных доходов
    """

    ri_id = '1'
    sum_regular_income = '0'

    def __init__(self):
        self.last_line = DB.ReadFromTable().get_last_regular_income()
        self.check_sum()

    def check_sum(self):
        """
        Пересчитывает сумму всех регулярных доходов
        """

        if self.last_line:
            all_regular_income = DB.ReadFromTable().read_regular_income()
            for line in all_regular_income:
                self.sum_regular_income = str(int(self.sum_regular_income) + int(line[2]))

    def check_id(self):
        """
        Вычисляет id для последующей записи регулярных доходов
        """

        if self.last_line:
            self.ri_id = str(int(self.last_line[0]) + 1)

    def add_regular_income(self, value, category):
        """
        Добавляет запись о регулрных расходов в базу данных
        """

        self.check_id()
        DB.WriteToTable().write_regular_income(self.ri_id, value, category)


class SingleIncome:
    sum_single_income = '0'

    def __init__(self):
        pass


class RegularExpenses:
    sum_regular_expenses = '0'

    def __init__(self):
        pass


class SingleExpenses:
    """
    Класс для внесения записи разовых расходов и определения таблицы для внесения записи
    """

    expenses_id = '1'
    day_id = '1'

    def __init__(self, category, value):
        self.date = str(datetime.date.today())
        # self.date = '2022-05-28'  # (Данная строка кода нужна только при тестировании)
        self.category = category
        self.value = value

        self.last_expenses = DB.ReadFromTable().get_last_expenses()
        self.last_day_expenses = DB.ReadFromTable().get_last_month_expenses()

        self.write = DB.WriteToTable()


    def change_day(self):
        """
        Смена даты
        """

        calc = Calculate()

        DB.CreateLog().write_day_log()
        self.check_last_day_expenses()
        self.write.write_month_expenses(self.day_id, self.date, calc.sum_day_expenses(), calc.budget(), calc.balance()
        # Перенести баланс в конце дня в разовые доходы
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
