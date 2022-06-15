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

        self.commands = {
            '/RI': self.ri,
            '/readRI': self.read_ri,
            '/delRI': self.del_ri,
            '/SI': self.si,
            '/readSI': self.read_si,
            '/delSI': self.del_si,
            '/RE': self.re,
            '/readRE': self.read_re,
            '/delRE': self.del_re,
            '/readDAY': self.read_day,
            '/readMON': self.read_mon,
            '/delDAY': self.del_day
        }

    def ri(self):
        RegularIncome().add_regular_income(self.text[2], self.text[1])
        self.answer = f'Даблен регулярный доход "{self.text[2]}" в количестве {self.text[1]} рублей'

    def read_ri(self):
        regular_income = DB.ReadFromTable().read_regular_income()
        answer_text = 'Пусто'
        if regular_income:
            answer_text = ''
            for line in regular_income:
                answer_text += str(line).strip('(').strip(')') + '\n'
        self.answer = answer_text

    def del_ri(self):
        category = self.text[1]
        DB.DeleteFromTable().delete_regular_income(category)
        self.answer = f'Регулярный доход "{category}" удален'

    def si(self):
        SingleIncome().add_single_income(self.text[2], self.text[1])
        self.answer = f'Добавлен разовый доход "{self.text[2]}" в размере {self.text[1]} рублей'

    def read_si(self):
        single_income = DB.ReadFromTable().read_single_income()
        answer_text = 'Пусто'
        if single_income:
            answer_text = ''
            for line in single_income:
                answer_text += str(line).strip('(').strip(')') + '\n'
        self.answer = answer_text

    def del_si(self):
        category = self.text[1]
        DB.DeleteFromTable().delete_single_income(category)
        self.answer = f'"{category}" удален из разовых доходов'

    def re(self):
        RegularExpenses().add_regular_expenses(self.text[2], self.text[1])
        self.answer = f'"{self.text[2]}" в количестве {self.text[1]} рублей добавлено в регулярные расходы'

    def read_re(self):
        regular_expenses = DB.ReadFromTable().read_regular_expenses()
        answer_text = 'Пусто'
        if regular_expenses:
            answer_text = ''
            for line in regular_expenses:
                answer_text += str(line).strip('(').strip(')') + '\n'
        self.answer = answer_text

    def del_re(self):
        category = self.text[1]
        DB.DeleteFromTable().delete_regular_expenses(category)
        self.answer = f'"{category}" удален из регулярных расходов'
    
    def read_day(self):
        day_expenses = DB.ReadFromTable().read_day_expenses()
        answer_text = 'Пусто'
        if day_expenses:
            answer_text = ''
            for line in day_expenses:
                answer_text += str(line).strip('(').strip(')') + '\n'
        self.answer = answer_text

    def read_mon(self):
        mon_expenses = DB.ReadFromTable().read_month_expenses()
        answer_text = 'Пусто'
        if mon_expenses:
            answer_text = ''
            for line in mon_expenses:
                answer_text += str(line).strip('(').strip(')') + '\n'
        self.answer = answer_text

    def del_day(self):
        expense_id = self.text[1]
        DB.DeleteFromTable().delete_single_expenses(expense_id)
        self.answer = f'Запись под номером "{expense_id}" удалена из таблицы текущих расходов'

    def start(self):
        """
        Проверяет наличие команд в вденном тексте
        """
        
        if '/' in self.text[0] and self.text[0] in self.commands:
            """
            При наличии команды, выполняет соотвествующую ей функцию
            """
            
            return self.commands[self.text[0]]()

        elif len(self.text) == 2:
            """
            При отсутствии команды делает запись в разовые расходы
            """

            if self.text[0].isdigit():
                setattr(self, 'value', self.text[0])
                setattr(self, 'category', self.text[1])
            else:
                setattr(self, 'value', self.text[1])
                setattr(self, 'category', self.text[0])

            SE = SingleExpenses(self.category, self.value)
            SE.write_single_expenses()

            self.answer = f'Бюджет на день {Calculate().budget() + Calculate().single.today_income} рублей\nРасходов за сегодня {Calculate().sum_day_expenses()} рублей\nЖелательно потратить не больше чем {Calculate().balance()} рублей'


class Calculate:
    """
    Проведение подсчетов
    """

    def __init__(self):
        self.reader = DB.ReadFromTable()
        self.days = calendar.monthrange(int(str(datetime.date.today())[:4]), int(str(datetime.date.today())[5:7]))[1]
        self.single = SingleIncome()
        self.single.check_income()

    def sum_day_expenses(self):
        """
        Сумма всех расходов в течение дня
        """

        expenses_list = [int(row[-1]) for row in self.reader.read_day_expenses() if row[-1].isdigit()]
        return str(sum(expenses_list))

    def budget(self):
        """
        (Регулярные доходы + разовые доходы - регулярные расходы) и все это делить на количество дней в месяце
        """
        return str(round(int(RegularIncome().sum_regular_income) - int(RegularExpenses().sum_regular_expenses) / int(self.days)))

    def balance(self):

        return int(self.budget()) - int(self.sum_day_expenses()) + int(self.single.today_income)


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
    single_income_id = '1'
    today_income = '0'
    all_today_income = None

    def __init__(self):
        self.last_line = DB.ReadFromTable().get_last_single_income()

    def check_income(self):
        self.all_today_income = DB.ReadFromTable().get_today_income()
        if self.all_today_income:
            for line in self.all_today_income:
                self.today_income = str(int(self.today_income) + int(line[-1]))
    
    def check_id(self):
        if self.last_line:
            self.single_income_id = str(int(self.last_line[0]) + 1)

    def add_single_income(self, category, value):
        self.check_id()
        DB.WriteToTable().write_single_income(self.single_income_id, str(datetime.date.today()), category, value)


class RegularExpenses:
    re_id = '1'
    sum_regular_expenses = '0'

    def __init__(self):
        self.last_line = DB.ReadFromTable().get_last_regular_expenses()
        self.check_sum()
    
    def check_sum(self):
        if self.last_line:
            all_regular_expenses = DB.ReadFromTable().read_regular_expenses()
            for line in all_regular_expenses:
                self.sum_regular_expenses = str(int(self.sum_regular_expenses) + int(line[2]))

    def check_id(self):
        if self.last_line:
            self.re_id = str(int(self.last_line[0]) + 1)

    def add_regular_expenses(self, category, value):
        self.check_id()
        DB.WriteToTable().write_regular_expenses(self.re_id, category, value)


class SingleExpenses:
    """
    Класс для внесения записи разовых расходов и определения таблицы для внесения записи
    """

    expenses_id = '1'
    day_id = '1'

    def __init__(self, category, value):
        self.date = str(datetime.date.today())
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
        self.write.write_month_expenses(self.day_id, self.date, calc.sum_day_expenses(), calc.budget(), calc.balance())
        SingleIncome().add_single_income('Остаток с прошлого дня', calc.balance())
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
