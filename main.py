import core
import working_with_databases


class ConsoleApp:
    def __init__(self, entry_data):
        self.expenses_data = entry_data.split()
        self.for_table = core.SingleExpenses(self.expenses_data[1], self.expenses_data[0])
        self.last_line = working_with_databases.get_last_line()

    def date_check(self):
        if not self.last_line:
            return True
        return str(self.for_table.date) == str(self.last_line[1])

    def write_expenses(self):
        if not self.last_line:
            self.for_table.expenses_id = '0'
        else:
            self.for_table.expenses_id = str(int(self.last_line[0]) + 1)
        self.for_table.write_data()


def main():
    while True:
        entry_data = input()
        if entry_data == 'exit':
            break
        else:
            app = ConsoleApp(entry_data)
            if app.date_check():
                app.write_expenses()
                print(app.last_line)
                print(working_with_databases.get_last_line())
            else:
                pass
                # working_with_databases.write_day_log()
                # Записать данные в таблицу расходов за месяц
                # Удалить таблицу расходов за день или все записи из нее
                # app.write_income()


if __name__ == '__main__':
    main()
