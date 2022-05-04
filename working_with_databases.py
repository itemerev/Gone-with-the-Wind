import sqlite3

conn = sqlite3.connect('gone_wind.db')
cur = conn.cursor()


def create_day_income():
    cur.execute('''CREATE TABLE IF NOT EXISTS day_income(
        single_income_id INT PRIMARY KEY,
        date TEXT,
        category TEXT,
        value TEXT);    
    ''')


def create_month_income():
    cur.execute('''CREATE TABLE IF NOT EXISTS month_income(
        day_income_id INT PRIMARY KEY,
        date TEXT,
        amount_per_day TEXT,
        budget_for_day TEXT,
        balance TEXT);    
    ''')


def write_single_income(single_income_id, date, category, value):
    day_income = (single_income_id, date, category, value)
    cur.execute("INSERT INTO day_income VALUES(?, ?, ?, ?);", day_income)
    conn.commit()


def write_month_income(day_income_id, date, amount_per_day, budget_for_day, balance):
    month_income = (day_income_id, date, amount_per_day, budget_for_day, balance)
    cur.execute("INSERT INTO month_income VALUES(?, ?, ?, ?, ?);", month_income)
    conn.commit()


def get_last_line():
    cur.execute('SELECT * FROM day_income ORDER BY single_income_id DESC LIMIT 1;')
    last_line = cur.fetchone()
    return last_line

def write_day_log():
    cur.execute('SELECT * FROM day_income')
    all_line = cur.fetchall()
    log_date = all_line[0][1]
    with open(f'Logs/{log_date}.txt', 'w', encoding='utf-8') as log_file:
        for line in all_line:
            log_file.write(str(line) + '\n')

