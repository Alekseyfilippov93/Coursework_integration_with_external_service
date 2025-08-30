import requests
from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def setup_method(self):
        self.api = HeadHunterAPI()

    @patch('src.api.requests.get')
    def test_get_vacancy_basic(self, mock_get):
        """Тест для получения вакансий"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "description": "Test description",
                    "snippet": {"requirement": "Test requirements"}
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancy("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"

    @patch('src.api.requests.get')
    def test_get_vacancy_empty(self, mock_get):
        """Тест пустого ответа"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancy("Python")

        assert len(vacancies) == 0

    @patch('src.api.requests.get')
    def test_get_vacancy_error(self, mock_get):
        """Тест ошибки запроса"""
        mock_get.side_effect = Exception("Error")

        vacancies = self.api.get_vacancy("Python")

        assert len(vacancies) == 0

def test_hh_api():
    url = "https://api.hh.ru/vacancies"
    params = {"text": "Менеджер", "page": 0, "per_page": 10}
    headers = {"User-Agent": "HH-User-Agent"}

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")

        data = response.json()
        print(f"Keys in response: {data.keys()}")
        print(f"Found vacancies: {data.get('found', 0)}")
        print(f"Items count: {len(data.get('items', []))}")

        if data.get("items"):
            print(f"First vacancy: {data['items'][0]['name']}")

    except Exception as e:
        print(f"Error: {e}")