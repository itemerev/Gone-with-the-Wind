import core
import get_and_write


class ConsoleApp:
    def __init__(self, entry_data):
        self.income_data = entry_data.split()
        self.last_line = get_and_write.get_last_line()
        self.for_table = core.SingleIncome(self.income_data[1], self.income_data[0])

    def date_check(self):
        return str(self.for_table.date) == str(self.last_line[1])

    def write_income(self):
        if not self.last_income:
            self.for_table.income_id = '0'
        else:
            self.for_table.income_id = str(int(self.last_line[0]) + 1)
            self.for_table.write_data()


def main():
    while True:
        entry_data = input()
        if entry_data == 'exit':
            break
        else:
            app = ConsoleApp(entry_data)
            if app.date_check():
                app.write_income()
                print(app.last_line)
                print(get_and_write.get_last_line())


if __name__ == '__main__':
    main()
