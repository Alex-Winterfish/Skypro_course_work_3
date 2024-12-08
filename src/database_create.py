import psycopg2
from src.vacancy_processing import HeadHunterVacancy
from src.vacancy_processing import employer_list
connection = {
    'host':'localhost',
    'database':'vacancies',
    'user':'postgres',
    'password':'101591910'
}
def create_tables():
    '''Функция создает таблицы employers и vacancies'''
    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE employers"
                        "("
                        "company_id SERIAL PRIMARY KEY,"
                        "company_name VARCHAR(100),"
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
                        ")")

            conn.commit()




def table_insert_value(vacancy:HeadHunterVacancy):
    employer_data = tuple(vacancy.employer_info)
    vacancy_data = vacancy.vacancy_list

    with psycopg2.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO employers("
                        "company_name, "
                        "description,"
                        " site_url,"
                        " city"
                        ") VALUES(%s, %s, %s, %s)", employer_data)

            for vac in vacancy_data:
                cur.execute("INSERT INTO vacancies("
                            "vacancy_name,"
                            "city, address,"
                            "vacancy_url,"
                            "requirement,"
                            "responsibilities,"
                            "schedule,"
                            "salary"
                            ") VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", vac)


            conn.commit()






if __name__ == '__main__':

    create_tables()
    data = HeadHunterVacancy(employer_list[0])

    table_insert_value(data)