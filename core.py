import datetime
import working_with_databases


class RegularIncome:
    pass


class SingleIncome:
    pass


class RegularExpenses:
    pass


class SingleExpenses:
    expenses_id = 0

    def __init__(self, category, value):
        working_with_databases.create_day_expenses()

        self.date = datetime.date.today()
        self.category = category
        self.value = value

    def write_data(self):
        working_with_databases.write_single_expenses(self.expenses_id, self.date, self.category, self.value)
