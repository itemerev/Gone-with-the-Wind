import datetime
import working_with_databases


class SingleIncome:
    income_id = 0

    def __init__(self, category, value):
        self.date = datetime.date.today()
        self.category = category
        self.value = value

        working_with_databases.create_day_income()

    def write_data(self):
        working_with_databases.write_single_income(self.income_id, self.date, self.category, self.value)
        self.income_id = str(int(self.income_id) + 1)


class ConstantIncome:
    pass
