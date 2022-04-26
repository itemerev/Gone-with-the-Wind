import datetime
import get_and_write


class SingleIncome:
    income_id = 0

    def __init__(self, category, value):
        self.date = datetime.date.today()
        self.category = category
        self.value = value

        get_and_write.create_day_income()

    def write_data(self):
        get_and_write.write_single_income(self.income_id, self.date, self.category, self.value)
        self.income_id += 1


class ConstantIncome:
    pass
