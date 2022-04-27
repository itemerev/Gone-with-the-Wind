import core
import get_and_write

while True:
    data = input()
    
    if data == 'exit':
        break

    else:
        income_data = data.split()
        last_income = get_and_write.get_one_income()

        income = core.SingleIncome(income_data[1], income_data[0])
        if not last_income:
            income.income_id = '0'
        else:
            print(last_income[0], income.income_id)
            income.income_id = str(int(last_income[0]) + 1)
        if not last_income or str(income.date) == str(last_income[1]):
            income.write_data()
            del income
        print(get_and_write.get_one_income())

