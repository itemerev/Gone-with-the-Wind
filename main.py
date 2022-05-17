import core
import working_with_databases as db


class ConsoleApp:
    """
    Взаимодействие с пользователем через консоль (терминал) в качестве проверки работоспособности ядра программы
    """

    def __init__(self):
        self.create_table()

        self.data = input()

    def create_table(self):
        """
        Создание таблиц в базе данных, если их не существует
        """

        create = db.CreateTables()
        create.create_regular_income()
        create.create_day_expenses()
        create.create_month_expenses()

    def run(self):
        """
        Главный цикл работы приложения (для завершения работы необходимо ввести команду 'exit')
        """

        while self.data != 'exit':
            one_event = core.Event(self.data)
            one_event.start()

            self.data = input()


if __name__ == '__main__':
    app = ConsoleApp()
    app.run()
