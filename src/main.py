from src.support_func import user_operation, user_interaction, user_database_interaction
from src.database_create import create_database, create_tables, table_insert_value
from src.vacancy_processing import HeadHunterVacancy
import json


def main():
    """Функция взаимодействия с пользователем"""

    while (
        True
    ):  # В цикле выясняем у пользователя необходимость создания таблиц в базе данных

        operation_choice = user_operation()
        if operation_choice in ["1", "2"]:
            break

    if operation_choice == "1":

        create_database()  # создаем базу данных
        create_tables()  # создаем таблицы в базе данный

        with open("../data/employers.json", "r+") as file:
            data = json.load(file)
        employer_list = list()

        for employer in data.values():
            employer_list.append(employer)

        for employer in employer_list:  # цикл для добавления данных в таблицу

            vacancies = HeadHunterVacancy(employer)
            table_insert_value(
                vacancies
            )  # вносим в таблицы данные о работодателях и их вакансии

    while True:  # В цикле запрашиваем у пользователя дейсвие с вакансиями

        user_input = user_interaction()
        if user_input in ["1", "2", "3", "4", "5"]:
            break

    data = user_database_interaction(user_input)

    return data

if __name__ == "__main__":

    print(main())
