import sqlite3

conn = sqlite3.connect('gone_wind.db')
cur = conn.cursor()


def create_day_expenses():
    cur.execute('''CREATE TABLE IF NOT EXISTS day_expenses(
        single_expenses_id INT PRIMARY KEY,
        date TEXT,
        category TEXT,
        value TEXT);    
    ''')


def create_month_expenses():
    cur.execute('''CREATE TABLE IF NOT EXISTS month_expenses(
        day_expenses_id INT PRIMARY KEY,
        date TEXT,
        amount_per_day TEXT,
        budget_for_day TEXT,
        balance TEXT);    
    ''')


def write_single_expenses(single_expenses_id, date, category, value):
    day_expenses = (single_expenses_id, date, category, value)
    cur.execute("INSERT INTO day_expenses VALUES(?, ?, ?, ?);", day_expenses)
    conn.commit()


def write_month_expenses(day_expenses_id, date, amount_per_day, budget_for_day, balance):
    month_expenses = (day_expenses_id, date, amount_per_day, budget_for_day, balance)
    cur.execute("INSERT INTO month_expenses VALUES(?, ?, ?, ?, ?);", month_expenses)
    conn.commit()


def get_last_line():
    cur.execute('SELECT * FROM day_expenses ORDER BY single_expenses_id DESC LIMIT 1;')
    last_line = cur.fetchone()
    return last_line


def write_day_log():
    cur.execute('SELECT * FROM day_expenses')
    all_line = cur.fetchall()
    log_date = all_line[0][1]
    with open(f'Logs/{log_date}.txt', 'w', encoding='utf-8') as log_file:
        for line in all_line:
            log_file.write(str(line) + '\n')

