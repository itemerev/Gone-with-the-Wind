import core
import working_with_databases as DB


def main():
    reader = DB.ReadFromTable()

    reader.read_day_expenses()
    print('----------')
    for i in reader.all_line:
        print(i)

    reader.read_month_expenses()
    print('----------')
    for j in reader.all_month:
        print(j)

    # DB.ClearTable().clear_day_expenses()
    # DB.ClearTable().clear_month_expenses()

    # test = core.Event('100 taxi')
    # test.start()
    
    # test = core.SingleExpenses('taxi', '100')
    # test.date = '2022-05-10'
    # test.write_single_expenses()
    #
    # test = core.SingleExpenses('food', '110')
    # test.date = '2022-05-10'
    # test.write_single_expenses()
    #
    # test = core.SingleExpenses('gas', '220')
    # test.date = '2022-05-11'
    # test.write_single_expenses()
    #
    # test = core.SingleExpenses('mas', '230')
    # test.date = '2022-05-11'
    # test.write_single_expenses()
    #
    # test = core.SingleExpenses('oil', '350')
    # test.date = '2022-05-12'
    # test.write_single_expenses()
    #
    # test = core.SingleExpenses('other', '360')
    # test.date = '2022-05-12'
    # test.write_single_expenses()
    #
    # reader = DB.ReadFromTable()
    # reader.read_day_expenses()
    # reader.read_month_expenses()
    #
    # print(*reader.all_line)
    # print('---------')
    # print(*reader.all_month)
    # print('---------')


if __name__ == '__main__':
    main()
