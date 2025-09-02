import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.abstract_classes import AbstractSaver
from src.vacancy import Vacancy


class JSONSaver(AbstractSaver):
    """Класс для сохранения информации о вакансиях в JSON-файл.
    Реализует абстрактные методы AbstractSaver.
    """

    def __init__(self, filename: str = "vacancies.json"):
        """Инициализация JSON-файла куда будет записываться."""
        self.__filename = filename
        self.__ensure_data_directory()

    def __ensure_data_directory(self) -> None:
        """Создаем папку data, если она не создана еще"""
        data_path = Path(__file__).parent.parent / "data"
        data_path.mkdir(exist_ok=True)
        self.__filepath = data_path / self.__filename

    def _read_vacancies(self) -> List[Dict]:
        """Прочитать вакансии из JSON-файла."""
        if not self.__filepath.exists():
            return []

        try:
            with open(self.__filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict]) -> None:
        """Записать вакансии в JSON-файл."""
        with open(self.__filepath, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в JSON-файл."""
        vacancies = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты
        duplicate = False
        for existing_vacancy in vacancies:
            if (
                existing_vacancy["title"] == vacancy_dict["title"]
                and existing_vacancy["url"] == vacancy_dict["url"]
            ):
                duplicate = True
                break

        if not duplicate:
            vacancies.append(vacancy_dict)
            self._write_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии из файла по критериям."""
        vacancies_data = self._read_vacancies()
        vacancies = []

        for vacancy_dict in vacancies_data:
            vacancy = Vacancy(
                title=vacancy_dict["title"],
                url=vacancy_dict["url"],
                salary_from=vacancy_dict["salary_from"],
                salary_to=vacancy_dict["salary_to"],
                currency=vacancy_dict["currency"],
                description=vacancy_dict["description"],
                requirements=vacancy_dict["requirements"],
            )
            vacancies.append(vacancy)

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if key == "min_salary":
                    if vacancy.salary_from < value:
                        match = False
                        break
                elif key == "max_salary":
                    if vacancy.salary_to > value:
                        match = False
                        break
                elif key == "keyword":
                    if (
                        value.lower() not in vacancy.title.lower()
                        and value.lower() not in vacancy.description.lower()
                    ):
                        match = False
                        break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из JSON-файла."""
        vacancies = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Удаляем вакансию
        new_vacancies = []
        for v in vacancies:
            if not (
                v["title"] == vacancy_dict["title"] and v["url"] == vacancy_dict["url"]
            ):
                new_vacancies.append(v)

        self._write_vacancies(new_vacancies)

    def clear_all(self) -> None:
        """Очистить все вакансии из файла."""
        self._write_vacancies([])
