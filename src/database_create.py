# coding=UTF-8
import os

import psycopg2
from src.vacancy_processing import HeadHunterVacancy
from dotenv import load_dotenv

load_dotenv()


def create_database():
    """Функция создает базу данных vacancies"""
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.getenv("PASSWORD"),
        host="localhost",
        port="5432",
    )

    cur = conn.cursor()

    conn.autocommit = True

    sql = "CREATE DATABASE vacancies"

    cur.execute(sql)

    cur.close()
    conn.close()


def create_tables():
    """Функция создает таблицы employers и vacancies"""

    connection = {
        "host": "localhost",
        "database": "vacancies",
        "user": "postgres",
        "password": os.getenv("PASSWORD"),
    }

    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE employers"
                "("
                "company_id SERIAL PRIMARY KEY,"
                "company_name VARCHAR(100) UNIQUE,"
                "description VARCHAR,"
                "site_url VARCHAR,"
                "city VARCHAR"
                ");"
                "CREATE TABLE vacancies"
                "("
                "company_id INT,"
                "vacancy_id SERIAL PRIMARY KEY,"
                "vacancy_name VARCHAR(100),"
                "city VARCHAR(100),"
                "address VARCHAR(100),"
                "vacancy_url VARCHAR(100),"
                "requirement TEXT,"
                "responsibilities TEXT,"
                "schedule VARCHAR(20),"
                "salary INT,"
                "FOREIGN KEY (company_id) REFERENCES employers(company_id)"
                ")"
            )

            conn.commit()


def table_insert_value(vacancy: HeadHunterVacancy):
    """Функция вносит данные в созданные таблицы"""
    connection = {
        "host": os.getenv("HOST"),
        "database": "vacancies",
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
    }

    employer_data = tuple(vacancy.employer_info)
    vacancy_data = vacancy.vacancy_list

    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employers("
                "company_name, "
                "description,"
                " site_url,"
                " city"
                ") VALUES(%s, %s, %s, %s)",
                employer_data,
            )

            conn.commit()

        with conn.cursor() as cur:
            for vac in vacancy_data:

                cur.execute(
                    "INSERT INTO vacancies("
                    "company_id)"
                    "SELECT company_id "
                    f"FROM employers WHERE company_name = '{employer_data[0]}'; "
                    "UPDATE vacancies "
                    "SET "
                    f"vacancy_name = '{vac[0]}',"
                    f"city = '{vac[1]}',"
                    f"address = '{vac[2]}',"
                    f"vacancy_url = '{vac[3]}',"
                    f"requirement = '{vac[4]}',"
                    f"responsibilities = '{vac[5]}',"
                    f"schedule = '{vac[6]}', "
                    f"salary = {vac[7]} "
                    f"WHERE vacancy_name IS NULL"
                )

            conn.commit()
