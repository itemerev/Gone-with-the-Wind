import core
import working_with_databases as DB


def main():
    DB.ClearTable().clear_day_expenses()
    DB.ClearTable().clear_month_expenses()
    
    test = core.SingleExpenses('taxi', '100')
    test.date = '2022-05-10'
    test.write_single_expenses()

    test = core.SingleExpenses('food', '110')
    test.date = '2022-05-10'
    test.write_single_expenses()

    test = core.SingleExpenses('gas', '220')
    test.date = '2022-05-11'
    test.write_single_expenses()

    test = core.SingleExpenses('mas', '230')
    test.date = '2022-05-11'
    test.write_single_expenses()

    test = core.SingleExpenses('oil', '350')
    test.date = '2022-05-12'
    test.write_single_expenses()

    test = core.SingleExpenses('other', '360')
    test.date = '2022-05-12'
    test.write_single_expenses()

    reader = DB.ReadFromTable()
    reader.read_day_expenses()
    reader.read_month_expenses()

    print(*reader.all_line)
    print('---------')
    print(*reader.all_month)

if __name__ == '__main__':
    main()