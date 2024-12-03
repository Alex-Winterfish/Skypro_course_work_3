from abc import ABC, abstractmethod

import requests


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




class HeadHunterAPI(VacancyAPI):


    def __init__(self, vacancy):
        self.__url = 'https://api.hh.ru/vacancies?employer_id=869045'
        self.__headers = {'User-Agent':'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        self.__vacancy = vacancy
        super().__init__(vacancy)

    def _api_request(self):
        super()._api_request()
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
        super()._get_vacancies()
        self.__params['text'] = self.__vacancy
        try:
            while self.__params.get('page') != 20:

                vacancies = self._api_request()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] +=1

            return self.__vacancies
        except Exception as e:
            print(f'Ошибка {e} в методе vacancies_request')

    @property
    def vacancy_list(self):
        '''Модуль для формирования списка вакансий с Названием Вакансии, Минимальной зарплатой, Описанием требований
        к соискателю, Ссылкой на вакансию на HH.ru и графиком работы'''
        try:
            raw_list = self._get_vacancies #получаем список вакансий с ХХ.ру
            vac_list = [] #список для накопления кавансий
            for i in range(len(raw_list)): #в этом цикле перебераем элементы
                for key, value in raw_list[i].items(): #в этом цикле перебераем словарь
                        # для получения определенных критериев для вакансии
                    if key in ['name', 'salary', 'snippet', 'url', 'schedule']:
                        vac_list.append(value)
            result_list = [] #список для накопления итоговых значений
            for vac in vac_list:
                if type(vac) is dict: #если элемент списка словарь, получаем начальный уровень зарплаты и обязаностей
                    for key, value in vac.items():
                        if key == 'from': #получем минимальный размер зарплаты
                            result_list.append(value)
                        elif key == 'requirement': #получаем требования к специальности
                            result_list.append(value)
                        elif key == 'name': #получаем режим работы
                            result_list.append(value)
                        else:
                            continue
                else:
                    result_list.append(vac)
            output_list = []
            for i in range(0,len(result_list), 5): #цикл для формирования списка вакансий
                output_list.append(result_list[i:i+5])

            return output_list
        except TypeError as e:
            print(f'Ошибка {e} в модуле vacancy_list')





if __name__ == '__main__':
    vacancy = HeadHunterAPI('')
    print(vacancy._get_vacancies)
