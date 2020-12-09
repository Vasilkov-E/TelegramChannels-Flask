import sys
from app import User
from app import db_users
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable


def add(param):
    '''

    :param param: param[0] - fio; param[1] - login; param[2] - password
    :return:
    '''
    try:
        fio = param[0]
        login = param[1]
        password = param[2]
        u = User(fio=fio, login=login)
        u.set_password(password)
        session.add(u)
        session.commit()
        print(f"Користувач {login} успішно додан.")
        return 1


    except sqlalchemy.exc.IntegrityError:
        print(f"Користувач {fio} вже має логін.")
    except:
        print("Error: %s" % sys.exc_info()[0])
        print("Записати в базу данних не вийшло.")


def delete(param):
    '''

    :param param: param[0] - login
    :return:
    '''
    try:
        login = param[0]
        u = User.query.filter_by(login=login).first()
        if u != None:
            User.query.filter_by(login=login).delete()
            db_users.session.commit()
            print(f"{u.login} успішно видалений")
        else:
            print(f"Такого користувача не має.")
            return 1
    except:
        print("Error: %s" % sys.exc_info()[0])
        print("Видалити не вийшло.")
        return 1


def info_comand(param=None):
    print("\033[3m\033[33m Команди:\n"
          "add - для створення нового користувача\n"
          "delete - для видалення користувача\n"
          "help - паказати команди\n"
          "get_users - вивести усіх користувачів\n"
          "search - пошук\n\033[0m"
          )


def get_users(param):
    '''

    :param param: param[0] - fio; param[1] - login
    :return:
    '''
    th = ['ФІО', 'login']
    td = User.query.order_by(User.id)
    table = PrettyTable(th)
    for td_data in td:
        table.add_row([td_data.fio, td_data.login])
    print(table)
    return 1


def search(param):
    '''

    :param param: param[0] - fio; param[1] - login
    :return:
    '''
    th = ['ФІО', 'login']
    if param[0] != '' and param[1] != '':
        td = User.query.filter(User.fio.contains(param[0]) | User.login.contains(param[1]))
    elif param[0] != '':
        td = User.query.filter(User.fio.contains(param[0]))
    elif param[1] != '':
        td = User.query.filter(User.login.contains(param[1]))
    table = PrettyTable(th)
    for td_data in td:
        table.add_row([td_data.fio, td_data.login])
    print(table)
    return 1


def main():
    comand = {'add': [add, 'ФІО', 'login', 'password'],
              'delete': [delete, 'login'],
              'help': [info_comand],
              'search': [search, 'fio', 'login'],
              'get_users': [get_users]
              }

    inp = input("Введіть команду: ")
    if inp in comand:
        param = []
        for e in comand.get(inp):
            if type(e) == str:
                param.append(input(f"{e}: "))
        comand[inp][0](param)
        return main()
    else:
        print("Я не знаю такої команди")
        return main()


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    Session = sessionmaker(bind=engine)
    session = Session()
    info_comand()
    main()

