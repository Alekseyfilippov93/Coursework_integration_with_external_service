from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.saver import JSONSaver
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)


def user_interaction():
    """Основная функция для взаимодействия с пользователем."""
    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    # Инициализация API и Saver
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Шаг 1: Поисковый запрос
    search_query = input(
        "Введите поисковый запрос (например: 'Python developer'): "
    ).strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым!")
        return

    print("\nИщем вакансии...")

    # Получаем вакансии с HH.ru
    try:
        vacancies_data = hh_api.get_vacancy(search_query)
        print(f"Получено данных от API: {len(vacancies_data)} записей")
        if vacancies_data:
            print(f"Первая вакансия: {vacancies_data[0].get('name', 'Нет названия')}")

        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        if not vacancies:
            print("По вашему запросу вакансий не найдено.")
            return

        print(f"Найдено вакансий: {len(vacancies)}")

        # Сохраняем все найденные вакансии
        for vacancy in vacancies:
            json_saver.add_vacancy(vacancy)

        # Шаг 2: Фильтрация по ключевым словам
        filter_input = input(
            "\nВведите ключевые слова для фильтрации (через пробел, например: 'опыт Python'): "
        ).strip()
        filter_words = filter_input.split() if filter_input else []

        filtered_vacancies = filter_vacancies(vacancies, filter_words)
        print(
            f"После фильтрации по ключевым словам: {len(filtered_vacancies)} вакансий"
        )

        # Шаг 3: Фильтрация по зарплате
        salary_input = input(
            "\nВведите диапазон зарплат (например: '100000-150000' или оставьте пустым): "
        ).strip()

        salary_filtered_vacancies = get_vacancies_by_salary(
            filtered_vacancies, salary_input
        )
        print(
            f"После фильтрации по зарплате: {len(salary_filtered_vacancies)} вакансий"
        )

        # Шаг 4: Сортировка и выбор топ N
        sorted_vacancies = sort_vacancies(salary_filtered_vacancies)

        try:
            top_n = int(
                input("\nСколько топ вакансий показать? (введите число): ").strip()
            )
        except ValueError:
            print("Неверный формат числа. Будет показано 10 вакансий.")
            top_n = 10

        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Шаг 5: Вывод результатов
        print(f"\n{'=' * 60}")
        print(f"РЕЗУЛЬТАТЫ ПОИСКА: {len(top_vacancies)} вакансий")
        print(f"{'=' * 60}")

        print_vacancies(top_vacancies)

        # Сохранение отфильтрованных результатов
        save_choice = (
            input("\nСохранить отфильтрованные результаты в файл? (y/n): ")
            .strip()
            .lower()
        )
        if save_choice == "y":
            for vacancy in top_vacancies:
                json_saver.add_vacancy(vacancy)
            print("Результаты сохранены в файл 'data/vacancies.json'")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Пожалуйста, проверьте подключение к интернету и попробуйте снова.")


def main():
    """
    Главная функция программы.
    """
    while True:
        user_interaction()

        # Запрос на повторный поиск
        repeat = input("\nХотите выполнить новый поиск? (да/нет): ").strip().lower()
        if repeat != "да":
            print("До свидания!")
            break


if __name__ == "__main__":
    main()
