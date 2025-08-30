from unittest.mock import patch, mock_open
from src.saver import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.saver = JSONSaver("test_vacancies.json")
        self.test_vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Test description",
            requirements="Test requirements"
        )

    def test_add_vacancy_no_duplicate(self):
        """Тест добавления вакансии без дубликатов"""
        with patch('src.saver.JSONSaver._read_vacancies', return_value=[]):
            with patch('src.saver.JSONSaver._write_vacancies') as mock_write:
                self.saver.add_vacancy(self.test_vacancy)
                mock_write.assert_called_once()

    def test_add_vacancy_with_duplicate(self):
        """Тест добавления вакансии с дубликатом"""
        existing_vacancy = [{
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Test description",
            "requirements": "Test requirements"
        }]

        with patch('src.saver.JSONSaver._read_vacancies', return_value=existing_vacancy):
            with patch('src.saver.JSONSaver._write_vacancies') as mock_write:
                self.saver.add_vacancy(self.test_vacancy)
                mock_write.assert_not_called()  # Не должно записывать дубликат

    def test_get_vacancies_empty(self):
        """Тест получения вакансий из пустого файла"""
        with patch('src.saver.JSONSaver._read_vacancies', return_value=[]):
            vacancies = self.saver.get_vacancies()
            assert len(vacancies) == 0

    def test_get_vacancies_with_data(self):
        """Тест получения вакансий с данными"""
        test_data = [{
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Test description",
            "requirements": "Test requirements"
        }]

        with patch('src.saver.JSONSaver._read_vacancies', return_value=test_data):
            vacancies = self.saver.get_vacancies()
            assert len(vacancies) == 1
            assert vacancies[0].title == "Python Developer"

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        test_data = [{
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Test description",
            "requirements": "Test requirements"
        }]

        with patch('src.saver.JSONSaver._read_vacancies', return_value=test_data):
            with patch('src.saver.JSONSaver._write_vacancies') as mock_write:
                self.saver.delete_vacancy(self.test_vacancy)
                mock_write.assert_called_once_with([])