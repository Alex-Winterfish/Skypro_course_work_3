import requests


class HeadHunterVacancy:
    """Класс для получения вакансий работодателя"""

    def __init__(self, employer):

        self.__employer = employer
        self.__vacancies_url = (
            f"https://api.hh.ru/vacancies?employer_id={self.__employer}"
        )
        self.__employer_url = f"https://api.hh.ru/employers/{self.__employer}"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"page": 0, "per_page": 100}
        self.__vacancies = []

    def __api_request(self, req_vac=True):
        """Метод подключения к НН.ру"""
        try:
            if req_vac:
                response = requests.get(
                    self.__vacancies_url, headers=self.__headers, params=self.__params
                )

            else:
                response = requests.get(
                    self.__employer_url, headers=self.__headers, params=self.__params
                )

            if response.status_code == 200:
                api_data = response.json()
                return api_data
        except Exception as e:
            print(f"Ошибка {e} в модуле api_request {requests.status_code}")

    def _get_vacancies(self):
        """Модуль для получения вакансий с HeadHunter.ru"""
        employer_vacancy = self.__api_request()["items"]
        return employer_vacancy

    def _get_employer(self):
        employer = self.__api_request(req_vac=False)
        return employer

    @property
    def vacancy_list(self):
        """Модуль для формирования списка вакансий с Названием Вакансии, Минимальной зарплатой, Описанием требований
        к соискателю, Ссылкой на вакансию на HH.ru и графиком работы"""
        try:

            output_list = list()  # словарь для накопления вакансий

            data = self._get_vacancies()
            for vac in data:

                vac_data = list()  # список для данный одной вакансии
                vac_data.append(vac.get("name"))
                if vac.get("address", 0) is not None:
                    vac_data.append(vac.get("address", 0).get("city"))
                    vac_data.append(vac.get("address", 0).get("raw"))
                else:
                    vac_data.append(None)
                    vac_data.append(None)

                vac_data.append(vac.get("alternate_url"))
                vac_data.append(vac.get("snippet").get("requirement"))
                vac_data.append(vac.get("snippet").get("responsibility"))
                vac_data.append(vac.get("schedule").get("name"))
                if vac.get("salary") is not None:
                    if vac.get("salary").get("from") is not None:
                        vac_data.append(vac.get("salary").get("from"))
                    else:
                        vac_data.append(0)
                else:
                    vac_data.append(0)

                output_list.append(vac_data)

            return output_list

        except TypeError as e:
            print(f"Ошибка {e} в модуле vacancy_list")

    @property
    def employer_info(self):
        """Метод для получения информации о работодателя"""
        try:
            output_list = list()

            emp_data = self._get_employer()

            output_list.append(emp_data.get("name"))
            output_list.append(emp_data.get("description"))
            output_list.append(emp_data.get("site_url"))
            output_list.append(emp_data.get("area").get("name"))

            return output_list
        except TypeError as e:
            print(f"Ошибка {e} в модуле employer_info")
