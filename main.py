import core
import get_and_write


class ConsoleApp:
    def __init__(self, entry_data):
        self.income_data = entry_data.split()
        self.last_income = get_and_write.get_one_income()
        self.for_table = core.SingleIncome(self.income_data[1], self.income_data[0])

    def date_check(self):
        return str(self.for_table.date) == str(self.last_income[1])

    def write_income(self):
        if not self.last_income:
            self.for_table.income_id = '0'
        else:
            self.for_table.income_id = str(int(self.last_income[0]) + 1)
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
                print(app.last_income)
                print(get_and_write.get_one_income())


if __name__ == '__main__':
    main()
