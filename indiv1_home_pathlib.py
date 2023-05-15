#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import copy
import argparse
from datetime import datetime
from pathlib import Path


def save_workers(file_name, people_list):
    """
    Сохранение списка людей в json
    """
    # Сохранение файла данных в домашнем каталоге пользователя
    file_name = f"{str(Path.home())}/{str(file_name)}"
    # Проверка заданного имени файла
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Заданный формат файла не .json", file=sys.stderr)
        return False

    # Делаем копию списка, чтобы его не затронуть
    lst = copy.deepcopy(people_list)
    # Сериализация даты в строку для записи в файл
    list(lst)
    print(lst)
    for i in lst:
        i["birth"] = i["birth"].strftime("%d.%m.%Y")

    # Дамп в json списка
    with open(file_name, "w", encoding="utf-8") as f_out:
        json.dump(lst, f_out, ensure_ascii=False, indent=4)
    lst.clear()


def load_workers(file_name):
    """
    Загрузка списка людей из json
    """
    if file_name.split(".", maxsplit=1)[-1] != "json":
        print("Несоответствующий формат файла", file=sys.stderr)
        return []

    if not os.path.exists(f"{os.getcwd()}/{file_name}"):
        print("Заданного файла не существует!", file=sys.stderr)
        return []

    with open(file_name, "r", encoding="utf-8") as f_in:
        data = json.load(f_in)
        flag = True
        if flag:
            for i in data:
                i["birth"] = datetime.strptime(i["birth"], "%d.%m.%Y").date()
            return data
        else:
            return []


def add_people(people_list, name, pnumber, birth):
    """
    Добавить людей
    """
    birth = birth.split(".")
    birth_dt = datetime(int(birth[2]), int(birth[1]), int(birth[0]))
    people_list.append({"name": name, "pnumber": pnumber, "birth": birth_dt})
    return people_list


def display_people(people_list):
    """
    Вывести людей из списка
    """
    if people_list:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 14, "-" * 19
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^14} | {:^19} |".format(
                "№п/п", "Фамилия Имя", "Номер телефона", "Дата рождения"
            )
        )
        print(line)
        for nmbr, person in enumerate(people_list, 1):
            print(
                "| {:>4} | {:<30} | {:<14} | {:>19} |".format(
                    nmbr,
                    person.get("name", ""),
                    person.get("pnumber", ""),
                    person.get("birth", "").strftime("%d.%m.%Y"),
                )
            )
        print(line)
    else:
        print("Список людей пуст!")


def correct_date(print_month):
    """
    Скорректировать номер месяца
    """
    month_by_text = {
        "январь": "01",
        "февраль": "02",
        "март": "03",
        "апрель": "04",
        "май": "05",
        "июнь": "06",
        "июль": "07",
        "август": "08",
        "сентябрь": "09",
        "октябрь": "10",
        "ноябрь": "11",
        "декабрь": "12",
    }
    if print_month.isalpha():
        print_month.lower()
        for key, value in month_by_text.items():
            if key == print_month:
                print_month = value
    if len(print_month) == 1:
        return "0" + print_month
    else:
        return print_month


def select_people(people_list, correct_printed_month):
    """
    Выбрать людей по заданному месяцу рождения
    """
    result = []
    for person in people_list:
        birth = person.get("birth")
        if correct_printed_month == birth.strftime("%m"):
            result.append(person)
    return result


def main(command_line=None):
    """
    Основная функция программы
    """
    # Создать родительский парсер для определения имени файла
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    # Создать основной парсер командной строки
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version", action="version", version="%(prog)s alpha beta 0.0.1"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления данных человека
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Добавить нового человека"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Имя и фамилия человека",
        nargs="+",
    )
    add.add_argument("-p", "--pnumber", action="store", help="Номер телефона")
    add.add_argument(
        "-b",
        "--birth",
        action="store",
        type=str,
        required=True,
        help="Person's birthday date",
    )

    # Создать субпарсер для отображения всех людей
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Отобразить всех людей"
    )

    # Создать субпарсер для выбора людей
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Выбрать людей по их месяцу рождения",
    )

    select.add_argument(
        "-M",
        "--month",
        action="store",
        type=str,
        required=True,
        help="Номер месяца рождения",
    )

    # Выполнить разбор аргументов командной строки
    args = parser.parse_args(command_line)

    # Загрузить всех людей из файла, если файл существует
    is_dirty = False
    if os.path.exists(args.filename):
        people = load_workers(args.filename)
    else:
        people = []

    # Добавить данные человека
    if args.command == "add":
        people = add_people(
            people, " ".join(args.name), args.pnumber, args.birth
        )
        is_dirty = True

    # Отобразить всех людей
    elif args.command == "display":
        display_people(people)

    # Выбрать требуемых людей
    elif args.command == "select":
        printed_month = args.month
        corrected_month = correct_date(printed_month)
        selected = select_people(people, corrected_month)
        display_people(selected)

    # Сохранить данные в файл, если список был изменен.
    if is_dirty:
        save_workers(args.filename, people)


if __name__ == "__main__":
    main()
