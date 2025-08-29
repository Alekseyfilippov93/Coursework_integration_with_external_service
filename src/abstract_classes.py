from abc import ABC, abstractmethod
from typing import List, Dict

class AbstractAPI(ABC):
    """Класс для работы с API сайта HH по поиску работы"""
    @abstractmethod
    def get_vacancy(self, search_query: str) -> List[Dict]:
        """Абстрактный метод для получения вакансий по запросу"""
        pass