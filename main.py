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
        self.entry_text = core.ParseInput(input())

    def run(self):
        """
        Главный цикл работы приложения (для завершения работы необходимо ввести команду 'exit')
        """

        while not self.entry_text.check_exit():
            if not self.entry_text.check_command():
                self.entry_text.parse_single_expenses()

                SE = core.SingleExpenses(self.entry_text.value, self.entry_text.category)
                SE.write_single_expenses()

            self.entry_text = core.ParseInput(input())


if __name__ == '__main__':
    app = ConsoleApp()
    app.run()
