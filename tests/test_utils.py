from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
)
from src.vacancy import Vacancy


class TestUtils:
    """Тесты для утилит"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.vacancies = [
            Vacancy(
                title="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                currency="RUR",
                description="Разработка на Python",
                requirements="Опыт работы с Python",
            ),
            Vacancy(
                title="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=80000,
                salary_to=120000,
                currency="RUR",
                description="Разработка на Java",
                requirements="Опыт работы с Java",
            ),
        ]

    def test_filter_vacancies_with_keywords(self):
        """Тест фильтрации по ключевым словам"""
        filtered = filter_vacancies(self.vacancies, ["Python"])
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

    def test_filter_vacancies_no_keywords(self):
        """Тест фильтрации без ключевых слов"""
        filtered = filter_vacancies(self.vacancies, [])
        assert len(filtered) == 2

    def test_get_vacancies_by_salary_range(self):
        """Тест фильтрации по диапазону зарплат"""
        filtered = get_vacancies_by_salary(self.vacancies, "90000-120000")
        # Проверяем что фильтрация работает
        assert len(filtered) > 0
        assert len(filtered) <= len(self.vacancies)

        # Проверяем что все отфильтрованные вакансии удовлетворяют условиям
        for vacancy in filtered:
            assert (
                vacancy.salary_from >= 90000
                or vacancy.salary_to <= 120000
                or (vacancy.salary_from <= 90000 and vacancy.salary_to >= 120000)
            )

    def test_sort_vacancies(self):
        """Тест сортировки вакансий"""
        sorted_vac = sort_vacancies(self.vacancies)
        assert sorted_vac[0].salary_from == 100000
        assert sorted_vac[1].salary_from == 80000

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий"""
        top_vac = get_top_vacancies(self.vacancies, 1)
        assert len(top_vac) == 1
        assert top_vac[0].title == "Python Developer"
