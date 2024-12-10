import psycopg2

host = 'localhost'
database = 'vacancies'
user = 'postgres'
password = '101591910'

class DBManager:

    def __init__(self, host, database, user, password):

        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self.__connection = {
            'host': self.__host,
            'database': self.__database,
            'user': self.__user,
            'password': self.__password
        }

    def get_companies_and_vacancies(self):

        with psycopg2.connect(**self.__connection) as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT company_name, "
                            "COUNT(vacancies.vacancy_name) "
                            "AS vacancies_count "
                            "FROM employers "
                            "JOIN vacancies "
                            "USING (company_id) "
                            "GROUP BY company_name")
                data = cur.fetchall()
                conn.commit()

        return data

    def get_all_vacancies(self):

        with psycopg2.connect(**self.__connection) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.company_name, "
                            "vacancy_name, "
                            "salary, "
                            "vacancy_url "
                            "FROM vacancies "
                            "JOIN employers "
                            "USING (company_id) "
                            "ORDER BY company_name")
                data = cur.fetchall()
                conn.commit()

            return data

    def get_avg_salary(self):

        with psycopg2.connect(**self.__connection) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary) "
                            "FROM vacancies "
                            "WHERE salary <> 0")

                data = cur.fetchall()

                conn.commit()

                avg_sal = round(float(data[0][0]), 2)

            return avg_sal

    def get_vacancies_with_higher_salary(self):

        with psycopg2.connect(**self.__connection) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT vacancy_name, "
                            "salary, "
                            "vacancy_url "
                            "FROM vacancies "
                            "WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary <> 0)"
                            "ORDER BY salary DESC")
                data = cur.fetchall()
                conn.commit()

        return data


if __name__ == '__main__':

    data = DBManager(host,database,user,password)

    list_vac = data.get_vacancies_with_higher_salary()

    print(list_vac)