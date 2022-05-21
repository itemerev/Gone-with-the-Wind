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
    
    print('----------')
    table = reader.read_regular_income()
    for k in table:
        print(k)


if __name__ == '__main__':
    main()
