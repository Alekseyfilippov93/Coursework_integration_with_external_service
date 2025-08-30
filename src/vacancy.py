from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Vacancy:
    """Класс для работы с вакансиями. В данном классе присутствует сравнение между вакансиями"""

    __slots__ = (
        "title",
        "url",
        "salary_from",
        "salary_to",
        "currency",
        "description",
        "requirements",
    )
    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency: Optional[str]
    description: str
    requirements: str

    def __post_init__(self):
        """Валидация данных, проверка указана ли зарплата или нет"""
        self._validate_salary()
        self._validate_url()

    def _validate_salary(self) -> None:
        """Приватный метод для валидации данных о зарплате"""
        # Если зарплата не указана - выставляем 0
        if self.salary_from is None:
            self.salary_from = 0
        if self.salary_to is None:
            self.salary_to = 0

        # Валидация отрицательных значений
        if self.salary_from < 0:
            self.salary_from = 0
        if self.salary_to < 0:
            self.salary_to = 0

        # Если обе границы 0 - значит зарплата не указана
        if self.salary_from == 0 and self.salary_to == 0:
            self.salary_from = None
            self.salary_to = None

    def _validate_url(self) -> None:
        """Приватный метод для валидации URL"""
        if not self.url.startswith(("http://", "https://")):
            self.url = f"https://{self.url}"

    def _validate_title(self) -> None:
        """Приватный метод для валидации названия вакансии"""
        if not self.title or self.title.strip() == "":
            self.title = "Название не указано"

    @property
    def salary(self) -> str:
        """Свойство для получения зарплаты в читаемом формате"""
        # Если обе границы равны 0 - значит зарплата не указана
        if self.salary_from == 0 and self.salary_to == 0:
            return "Зарплата не указана"

        if self.salary_from == self.salary_to:
            return f"{self.salary_from} {self.currency or 'руб.'}"
        else:
            return f"{self.salary_from}-{self.salary_to} {self.currency or 'руб.'}"

    def __lt__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (меньше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented

        # Сравниваем по минимальной зарплате
        return self.salary_from < other.salary_from

    def __gt__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (больше)"""
        if not isinstance(other, Vacancy):
            return NotImplemented

        return self.salary_from > other.salary_from

    def __eq__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented

        return self.salary_from == other.salary_from

    def __le__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (меньше или равно)"""
        return self < other or self == other

    def __ge__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (больше или равно)"""
        return self > other or self == other

    def __ne__(self, other: Any) -> bool:
        """Метод для сравнения вакансий по зарплате (не равно)"""
        return not self == other

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list[dict]) -> list["Vacancy"]:
        """
        Классовый метод для преобразования данных из API в список объектов Vacancy.
        """
        # vacancies_data: Список словарей с данными от API
        # return: Список объектов Vacancy

        vacancies_list = []

        for vacancy_data in vacancies_data:
            try:
                # Извлекаем данные о зарплате
                salary_info = vacancy_data.get("salary")
                if salary_info:
                    salary_from = salary_info.get("from")
                    salary_to = salary_info.get("to")
                    currency = salary_info.get("currency")
                else:
                    salary_from = salary_to = currency = None

                # Создаем объект вакансии
                vacancy = cls(
                    title=vacancy_data.get("name", "Не указано"),
                    url=vacancy_data.get("alternate_url", ""),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    description=(
                        vacancy_data.get("description", "")[:200] + "..."
                        if vacancy_data.get("description")
                        else "Не указано"
                    ),
                    requirements=vacancy_data.get("snippet", {}).get(
                        "requirement", "Не указано"
                    ),
                )
                vacancies_list.append(vacancy)

            except (KeyError, TypeError) as e:
                print(f"Ошибка при обработке вакансии: {e}")
                continue

        return vacancies_list

    def to_dict(self) -> dict:
        """Метод для преобразования объекта в словарь (для сохранения в JSON)"""
        return {
            "title": self.title,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "description": self.description,
            "requirements": self.requirements,
        }

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (
            f"Вакансия: {self.title}\n"
            f"Ссылка: {self.url}\n"
            f"Зарплата: {self.salary}\n"
            f"Требования: {self.requirements}\n"
            f"Описание: {self.description}"
        )
