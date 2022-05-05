import sqlite3


class Connect:
    """
    Подключение к базе данных
    (используется только как родительский класс)
    """
    def __init__(self):
        self.con = sqlite3.connect('gone_wind.db')
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()


class CreateTables(Connect):
    """
    Создание таблиц в БД
    """

    def create_regular_income(self):
        """
        Создание таблицы регулярных доходов
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS regular_income(
            regular_income_id INT PRIMARY KEY,
            name_income TEXT,
            value TEXT);
        ''')

    def create_single_income(self):
        """
        Создание таблицы разовых доходов
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS single_income(
            single_income_id INT PRIMARY KEY,
            date TEXT,
            name_income TEXT,
            value TEXT);
        ''')

    def create_regular_expenses(self):
        """
        Создание таблицы регулярных расходов
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS regular_expenses(
            regular_expenses_id INT PRIMARY KEY,
            category TEXT,
            value TEXT);
        ''')

    def create_day_expenses(self):
        """
        Создание таблицы расходов за день
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS day_expenses(
            single_expenses_id INT PRIMARY KEY,
            date TEXT,
            category TEXT,
            value TEXT);    
        ''')

    def create_month_expenses(self):
        """
        Создание таблицы расходов за месяц
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS month_expenses(
            day_expenses_id INT PRIMARY KEY,
            date TEXT,
            amount_per_day TEXT,
            budget_for_day TEXT,
            balance TEXT);    
        ''')


class WriteToTable(Connect):
    """
    Запись данных в БД
    """

    def write_single_expenses(self, single_expenses_id, date, category, value):
        """
        Запись разовых расходов в БД в таблицу расходов за день
        """

        day_expenses = (single_expenses_id, date, category, value)
        self.cur.execute("INSERT INTO day_expenses VALUES(?, ?, ?, ?);", day_expenses)
        self.con.commit()

    # Необходимо переименовать атрибут 'amount_per_day'
    def write_month_expenses(self, day_expenses_id, date, amount_per_day, budget_for_day, balance):
        """
        Запись суммы днеынх расходов в БД в таблицу расходов за месяц
        """

        # Необходимо переименовать атрибут 'amount_per_day'
        month_expenses = (day_expenses_id, date, amount_per_day, budget_for_day, balance)
        self.cur.execute("INSERT INTO month_expenses VALUES(?, ?, ?, ?, ?);", month_expenses)
        self.con.commit()


class ReadFromTable(Connect):
    """
    Чтение данных из БД
    """

    def __init__(self):
        super().__init__()

        self.last_expenses = None

        self.all_line = None
        self.log_date = None

    def get_last_expenses(self):
        """
        Чтение последней записи разовых расходов
        """

        cur.execute('SELECT * FROM day_expenses ORDER BY single_expenses_id DESC LIMIT 1;')
        self.last_expenses = cur.fetchone()

    def read_day_expenses(self):
        """
        Чтение всех расходов за день
        """

        self.cur.execute('SELECT * FROM day_expenses')
        self.all_line = cur.fetchall()
        self.log_date = all_line[0][1]


class CreateLog:
    """
    Логирование в текстовый файл
    """

    def __init__(self):
        self.day_expenses = ReadFromTable()

    def write_day_log(self):
        """
        Логирование всех расходов за день в файл '{дата}.txt'
        """

        self.day_expenses.read_day_expenses()
        with open(f'Logs/{self.day_expenses.log_date}.txt', 'w', encoding='utf-8') as log_file:
            for line in self.day_expenses.all_line:
                log_file.write(str(line) + '\n')

