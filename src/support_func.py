from database_access import DBManager
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("PASSWORD")


def user_operation():
    """Функция выясняет у пользователя необходимость создания таблиц в базе данных"""
    print("Добро пожаловать в программу обработки вакансий")
    user_input = input(
        "Какие операции выполнить?\n"
        "1 - Создание таблиц в базе данный\n"
        "2 - Работа с существующими таблицами\n"
    )
    return user_input


def user_interaction():
    """Функция запрашивает у пользователя, какие операции выполнить с вакансиями из файла"""
    user_input = input(
        "Какие операции выполнить? \n"
        "1 - Получить список всех компаний и количество вакансий в компаниях \n"
        "2 - Получить список всех вакансий с указанием названия компании,названия вакансии, "
        "зарплаты и ссылки на вакансию\n"
        "3 - Получить среднюю зарплату по вакансиям\n"
        "4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
        "5 - Найти вакансию по ключевому слову\n"
    )

    return user_input


def user_database_interaction(user_input: str):
    """Функция выполняет обработку вакансий из базы данных"""

    data_base = DBManager("localhost", "vacancies", "postgres", password)

    if user_input == "1":

        data = data_base.get_companies_and_vacancies_count

        return data

    elif user_input == "2":

        data = data_base.get_all_vacancies

        return data

    elif user_input == "3":

        data = data_base.get_avg_salary
        return data

    elif user_input == "4":

        data = data_base.get_vacancies_with_higher_salary

        return data

    elif user_input == "5":
        key_word = input("Введите ключевое слово для поиска: \n")

        data = data_base.get_vacancies_whit_keyword(key_word)
        return data
