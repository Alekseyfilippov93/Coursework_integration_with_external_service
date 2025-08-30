from typing import List
from src.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам в описании и требованиях."""
    # vacancies: Список вакансий
    # filter_words: Список ключевых слов для фильтрации

    if not filter_words:
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        # Проверяем каждое ключевое слово
        for word in filter_words:
            word_lower = word.lower()
            if (
                word_lower in vacancy.title.lower()
                or word_lower in vacancy.description.lower()
                or word_lower in vacancy.requirements.lower()
            ):
                filtered_vacancies.append(vacancy)
                break  # Если нашли одно совпадение, добавляем и выходим

    return filtered_vacancies


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """Фильтрует вакансии по диапазону зарплат."""
    if not salary_range.strip():
        return vacancies

    try:
        # Парсим диапазон зарплат
        if "-" in salary_range:
            min_salary, max_salary = map(int, salary_range.split("-"))
        else:
            min_salary = int(salary_range)
            max_salary = float("inf")

        filtered_vacancies = []
        for vacancy in vacancies:
            # Проверяем, попадает ли зарплата в диапазон
            vacancy_min = vacancy.salary_from or 0
            vacancy_max = vacancy.salary_to or float("inf")

            if (
                (vacancy_min >= min_salary and vacancy_min <= max_salary)
                or (vacancy_max >= min_salary and vacancy_max <= max_salary)
                or (vacancy_min <= min_salary and vacancy_max >= max_salary)
            ):
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    except ValueError:
        print(
            "Ошибка: Неверный формат диапазона зарплат. Используйте формат: '100000-150000'"
        )
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате (по убыванию)."""

    return sorted(
        vacancies, key=lambda x: (x.salary_from or 0, x.salary_to or 0), reverse=True
    )


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ N вакансий."""
    # vacancies: Список вакансий
    # top_n: Количество вакансий для возврата

    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит вакансии в читаемом формате."""

    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'=' * 60}")
        print(f"ВАКАНСИЯ {i}")
        print(f"{'=' * 60}")
        print(f"Должность: {vacancy.title}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Ссылка: {vacancy.url}")
        print(f"\nТребования: {vacancy.requirements}")
        print(f"\nОписание: {vacancy.description}")
        print(f"{'=' * 60}")
