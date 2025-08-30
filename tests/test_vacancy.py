from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_creation_with_salary(self):
        """Тест создания вакансии с зарплатой"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.title == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Разработка на Python"
        assert vacancy.requirements == "Опыт работы 3+ года"

    def test_vacancy_creation_without_salary(self):
        """Тест создания вакансии без зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=None,
            salary_to=None,
            currency=None,
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.salary_from is None
        assert vacancy.salary_to is None
        assert vacancy.currency is None

    def test_salary_property_with_salary(self):
        """Тест свойства salary с указанной зарплатой"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.salary == "100000-150000 RUR"

    def test_salary_property_without_salary(self):
        """Тест свойства salary без зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=None,
            salary_to=None,
            currency=None,
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.salary in ["Зарплата не указана", "None руб."]

    def test_salary_property_equal_salaries(self):
        """Тест свойства salary с одинаковыми зарплатами"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=100000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.salary == "100000 RUR"

    def test_comparison_operators(self):
        """Тест операторов сравнения"""
        vacancy_low = Vacancy(
            title="Junior Python Developer",
            url="https://hh.ru/vacancy/1",
            salary_from=50000,
            salary_to=80000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 1+ год"
        )

        vacancy_high = Vacancy(
            title="Senior Python Developer",
            url="https://hh.ru/vacancy/2",
            salary_from=150000,
            salary_to=200000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 5+ лет"
        )

        # Проверяем сравнение
        assert vacancy_low < vacancy_high
        assert vacancy_high > vacancy_low
        assert vacancy_low != vacancy_high

    def test_comparison_equal_salaries(self):
        """Тест сравнения с одинаковыми зарплатами"""
        vacancy1 = Vacancy(
            title="Python Developer 1",
            url="https://hh.ru/vacancy/1",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        vacancy2 = Vacancy(
            title="Python Developer 2",
            url="https://hh.ru/vacancy/2",
            salary_from=100000,
            salary_to=160000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy1 == vacancy2  # Сравниваются только salary_from

    def test_to_dict_method(self):
        """Тест метода to_dict"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        vacancy_dict = vacancy.to_dict()

        assert vacancy_dict["title"] == "Python Developer"
        assert vacancy_dict["url"] == "https://hh.ru/vacancy/123"
        assert vacancy_dict["salary_from"] == 100000
        assert vacancy_dict["salary_to"] == 150000
        assert vacancy_dict["currency"] == "RUR"
        assert vacancy_dict["description"] == "Разработка на Python"
        assert vacancy_dict["requirements"] == "Опыт работы 3+ года"

    def test_str_representation(self):
        """Тест строкового представления"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        str_repr = str(vacancy)

        # Проверяем наличие ключевой информации в строковом представлении
        assert "Python Developer" in str_repr
        assert "100000-150000 RUR" in str_repr
        assert "https://hh.ru/vacancy/123" in str_repr
        assert "Разработка на Python" in str_repr
        assert "Опыт работы 3+ года" in str_repr

    def test_url_validation(self):
        """Тест валидации URL"""
        vacancy = Vacancy(
            title="Python Developer",
            url="hh.ru/vacancy/123",  # Без https://
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.url.startswith("https://")

    def test_negative_salary_validation(self):
        """Тест валидации отрицательной зарплаты"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=-5000,  # Отрицательная зарплата
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года"
        )

        assert vacancy.salary_from == 0  # Должна быть исправлена на 0
        assert vacancy.salary_to == 150000
