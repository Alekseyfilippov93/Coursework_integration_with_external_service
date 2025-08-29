import requests
from typing import List, Dict
from src.abstract_classes import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для того чтобы мы смогли работать по API сайта HH.ru"""
    _URL_HH = "https://api.hh.ru/vacancies"  # URL API HeadHuntet

    def __init__(self):
        """Инициализируем класс для работы с API"""
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'text': '', 'page': 0, 'per_page': 100}

    def _get_data(self, search_query: str) -> List[Dict]:
        """Приватный метод для получения данных от API."""
        self._params['text'] = search_query
        self._params['page'] = 0
        try:
            response = requests.get(self._URL_HH, headers=self._headers, params=self._params)
            response.raise_for_status()  # Проверяем статус код
            return response.json()['items']
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []
        except KeyError as e:
            print(f"Ошибка при обработке ответа API: {e}")
            return []

    def get_vacancy(self, search_query: str) -> List[Dict]:
        """Публичный метод для получения вакансий."""
        vacancy = self._get_data(search_query)
        return vacancy


    # Пример использования (можно удалить после тестирования)
if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    vacancy = hh_api.get_vacancy("Python developer")
    print(f"Найдено вакансий: {len(vacancy)}")
    if vacancy:
        print(f"Первая вакансия: {vacancy[0]['name']}")
