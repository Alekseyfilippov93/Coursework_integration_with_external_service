import pytest
from src.abstract_classes import AbstractAPI, AbstractSaver


class TestAbstractClasses:
    """Тесты для абстрактных классов"""

    def test_abstract_api_cannot_be_instantiated(self):
        """Тест, что нельзя создать экземпляр AbstractAPI"""
        with pytest.raises(TypeError):
            AbstractAPI()

    def test_abstract_saver_cannot_be_instantiated(self):
        """Тест, что нельзя создать экземпляр AbstractSaver"""
        with pytest.raises(TypeError):
            AbstractSaver()

    def test_abstract_api_has_get_vacancy_method(self):
        """Тест, что AbstractAPI имеет метод get_vacancy"""
        assert hasattr(AbstractAPI, "get_vacancy")

    def test_abstract_saver_has_required_methods(self):
        """Тест, что AbstractSaver имеет все обязательные методы"""
        required_methods = ["add_vacancy", "get_vacancies", "delete_vacancy"]
        for method in required_methods:
            assert hasattr(AbstractSaver, method)


# Простые тестовые реализации
class TestAPI(AbstractAPI):
    def get_vacancy(self, search_query: str) -> list:
        return []


class TestSaver(AbstractSaver):
    def add_vacancy(self, vacancy) -> None:
        pass

    def get_vacancies(self, criteria=None) -> list:
        return []

    def delete_vacancy(self, vacancy) -> None:
        pass


def test_concrete_classes_can_be_instantiated():
    """Тест что конкретные реализации могут создаваться"""
    api = TestAPI()
    saver = TestSaver()

    assert isinstance(api, AbstractAPI)
    assert isinstance(saver, AbstractSaver)
    assert api.get_vacancy("test") == []
    assert saver.get_vacancies() == []
