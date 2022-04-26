import datetime


class SingleIncome:
    def __init__(self, category, value):
        self.date = datetime.date.today()
        self.category = category
        self.value = value


class ConstantIncome:
    pass
