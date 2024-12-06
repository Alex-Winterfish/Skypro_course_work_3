from abc import ABC, abstractmethod

import requests
import json


class VacancyAPI(ABC):

    @abstractmethod
    def __init__(self, vacancy):
        self.__vacancy = vacancy

    @abstractmethod
    def _api_request(self):
        pass

    @abstractmethod
    def _get_vacancies(self):
        pass

search_vacancy_url='https://api.hh.ru/vacancies?employer_id=869045'

search_employers_url='https://api.hh.ru/employers'

search_areas='https://api.hh.ru/areas'

cbs_commodities_management = "1162986"

encore = "5344909"

gts = "2029899"

happy_delivery = "11071056"

happy_phone = "3786114"

koblik_group = "40951"

ozon = "10690081"

retail_personal = "1420859"

rubin_aero_corp = "1035262"

abc_electro = "129348"

agat_utility =  "168386"

al_5 = "57302"

gijov_galary = "25331"

bel_gran = "602244"

benuk_se = "10911906"





class HeadHunterVacancy:


    def __init__(self, employer):

        self.__employer = employer
        self.__url = f'https://api.hh.ru/vacancies?employer_id={self.__employer}'
        self.__headers = {'User-Agent':'HH-User-Agent'}
        self.__params = {'text': '','only_with_vacancies': True, 'page': 0, 'per_page': 100}
        self.__vacancies = []

    def __api_request(self):
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)

            if response.status_code == 200:
                api_data = response.json()
                return api_data
        except Exception as e:
            print(f'Ошибка {e} в модуле api_request {requests.status_code}')

    @property
    def _get_vacancies(self):
        '''Модуль для получения вакансий с HeadHunter.ru'''
        employer_vacancy = self.__api_request()['items']
        return employer_vacancy

    @property
    def vacancy_list(self):
        '''Модуль для формирования списка вакансий с Названием Вакансии, Минимальной зарплатой, Описанием требований
        к соискателю, Ссылкой на вакансию на HH.ru и графиком работы'''
        try:

            output_dict=dict() #словарь для накопления вакансий
            i = 1
            data = self._get_vacancies
            for vac in data:

                vac_data=list() #список для данный одной вакансии
                vac_data.append(vac.get('name'))
                vac_data.append(vac.get('address', 0).get('city'))
                vac_data.append(vac.get('address', 0).get('raw'))
                vac_data.append(vac.get('alternate_url'))
                vac_data.append(vac.get('snippet').get('requirement'))
                vac_data.append(vac.get('snippet').get('responsibility'))
                vac_data.append(vac.get('schedule').get('name'))
                vac_data.append(vac.get('salary'))

                output_dict[i] = vac_data

                i+=1

            return output_dict



        except TypeError as e:
            print(f'Ошибка {e} в модуле vacancy_list')





if __name__ == '__main__':
    vacancy = HeadHunterVacancy(encore)
    data = vacancy.vacancy_list


    with open('dump.json', "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=1)

