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
            single_expenses_id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
            date TEXT,
            category TEXT,
            value TEXT);    
        ''')

    def create_month_expenses(self):
        """
        Создание таблицы расходов за месяц
        """

        self.cur.execute('''CREATE TABLE IF NOT EXISTS month_expenses(
            day_expenses_id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
            date TEXT,
            amount_per_day TEXT,
            budget_for_day TEXT,
            balance TEXT);    
        ''')


class WriteToTable(Connect):
    """
    Запись данных в БД
    """

    def write_single_expenses(self, date, category, value):
        """
        Запись разовых расходов в БД в таблицу расходов за день
        """

        day_expenses = (date, category, value)
        self.cur.execute("INSERT INTO day_expenses VALUES(NULL, ?, ?, ?);", day_expenses)
        self.con.commit()

    def write_month_expenses(self, date, expenses_per_day, budget_for_day, balance):
        """
        Запись суммы днеынх расходов в БД в таблицу расходов за месяц
        """

        month_expenses = (date, expenses_per_day, budget_for_day, balance)
        self.cur.execute("INSERT INTO month_expenses VALUES(NULL, ?, ?, ?, ?);", month_expenses)
        self.con.commit()


class ClearTable(Connect):
    def __init__(self):
        super().__init__()

    def clear_day_expenses(self):
        self.cur.execute("DELETE FROM day_expenses")
        self.con.commit()


class ReadFromTable(Connect):
    """
    Чтение данных из БД
    """

    def __init__(self):
        super().__init__()

        self.last_expenses = None
        self.last_day_expenses = None

        self.all_line = None
        self.log_date = None
        self.all_month = None

    def get_last_expenses(self):
        """
        Чтение последней записи разовых расходов
        """

        self.cur.execute('SELECT * FROM day_expenses ORDER BY single_expenses_id DESC LIMIT 1;')
        self.last_expenses = self.cur.fetchone()

    def get_last_month_expenses(self):
        self.cur.execute('SELECT * FROM month_expenses ORDER BY day_expenses_id DESC limit 1;')
        self.last_day_expenses = self.cur.fetchone()

    def read_day_expenses(self):
        """
        Чтение всех расходов за день
        """

        self.cur.execute('SELECT * FROM day_expenses')
        self.all_line = self.cur.fetchall()
        self.log_date = self.all_line[0][1]

    def read_month_expenses(self):
        
        self.cur.execute('SELECT * FROM month_expenses')
        self.all_month = self.cur.fetchall()


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

