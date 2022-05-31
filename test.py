
import os

# os.remove('gone_wind.db')

from bot import create_all_tables as cr
from core import *
import working_with_databases as DB

class TestEvent(Event):
    def start(self, date):
        if '/' in self.text[0]:
            return self.commands[self.text[0]]()

        elif self.text[0].isdigit():
            self.value = self.text[0]
            self.category = self.text[1]
        else:
            self.value = self.text[1]
            self.category = self.text[0]
        
        SE = SingleExpenses(self.category, self.value)
        SE.date = date
        SE.write_single_expenses()

        c = Calculate()
        self.answer = f'{c.budget()}, {c.sum_day_expenses()}, {c.balance()}'
 

def make_data():
    one_event = TestEvent('/RI 50000 testRI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/SI 1000 testSI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/RE 20000 testRE')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readRI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readSI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readRE')
    one_event.start(None)
    print(one_event.answer)
    print('-----------')
    testing()
    print('-----------')
    one_event = TestEvent('/delRI testRI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/delSI testSI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/delRE testRE')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readRI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readSI')
    one_event.start(None)
    print(one_event.answer)
    one_event = TestEvent('/readRE')
    one_event.start(None)
    print(one_event.answer)


def testing():
    for k in range(3):
        for j in range(5):
            date = f'2022-0{str(5 + k)}-0{str(1 + j)}'
            for i in range(5):
                one_event = TestEvent(f'210 test{str(i)}')
                one_event.start(date)
                print(one_event.answer)
            print('---')


if __name__ == '__main__':
    cr()
    make_data()
    os.remove('gone_wind.db')
    print(DB.ReadFromTable().get_today_income())




