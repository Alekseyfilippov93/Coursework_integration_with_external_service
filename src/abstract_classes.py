from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from src.vacancy import Vacancy


class AbstractAPI(ABC):
    """Класс для работы с API сайта HH по поиску работы"""

    @abstractmethod
    def get_vacancy(self, search_query: str) -> List[Dict]:
        """Абстрактный метод для получения вакансий по запросу"""
        pass


class AbstractSaver(ABC):
    """Абстрактный класс для добавлений вакансий в файл"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляем вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии из файла по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из файла."""
        pass
