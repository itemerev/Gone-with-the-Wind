import core
import working_with_databases as db


class ConsoleApp:
    """
    Взаимодействие с пользователем через консоль (терминал) в качестве проверки работоспособности ядра программы
    """

    create = db.CreateTables()
    create.create_day_expenses()
    create.create_month_expenses()

    def __init__(self):
        self.data = core.ParseInput(input())

    def run(self):
        """
        Главный цикл работы приложения (для завершения работы необходимо ввести команду 'exit')
        """

        while not self.data.check_exit():
            self.data.parse_single_expenses()

            SE = core.SingleExpenses(self.data.category, self.data.value)
            SE.write_single_expenses()

            self.data = core.ParseInput(input())


if __name__ == '__main__':
    app = ConsoleApp()
    app.run()
