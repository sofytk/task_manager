from datetime import datetime
from itertools import groupby
from domain.model.category import Category
from domain.model.priority import Priority
from domain.model.task import Task
from domain.controller.task_controller import TaskController


class Client:
    """
    Класс Клиента для взаимодействия пользователя с системой управления задачами
    """

    def __init__(self):
        """
        Инициализация клиента и запуск меню
        """
        self.controller = TaskController()
        self.show_menu()

    def show_menu(self):
        """
        Основной цикл меню
        """
        print("Привет! Менеджер задач запущен.")

        while True:
            print("--------------------------------")
            print("\nМеню:")
            print("1. Добавить задачу")
            print("2. Показать задачу на сегодня")
            print("3. Показать все задачи")
            print("4. Показать задачи на дату")
            print("5. Сортировка по приоритету")
            print("6. Сортировка по категории")
            print("7. Отметить задачу выполненной")
            print("8. Удалить задачу")
            print("9. Выход")

            choice = input("\nВыберите пункт: ").strip()
            print("")

            match choice:

                case "1":
                    self._add_task()

                case "2":
                    self._show_today_tasks()

                case "3":
                    self._show_all_tasks()

                case "4":
                    self._show_tasks_by_date()

                case "5":
                    self._sort_by_priority()

                case "6":
                    self._sort_by_category()

                case "7":
                    self._mark_task_done()

                case "8":
                    self._delete_task()

                case "9":
                    print("Выход. До свидания!")
                    break

                case _:
                    print("Неверный выбор. Попробуйте снова.")


    def _add_task(self):
        """Создание и добавление новой задачи"""
        date = self.input_date()
        title = input("Название: ").strip()
        description = input("Описание: ").strip()

        print("Приоритет задачи:")
        priority = self.choose_enum(Priority)

        print("Категория задачи:")
        category = self.choose_enum(Category)

        is_done_input = input("Статус - выполнено? [y/n]: ").strip().lower()
        is_done = is_done_input == "y"

        task = Task(date, title, description, priority, is_done, category)
        self.controller.add_task(task)
        print("Задача добавлена и сохранена.")

    def _show_all_tasks(self):
        """Вывод всех задач"""
        tasks = self.controller.get_all_tasks()
        self.display_tasks(tasks)
        input("\nНажмите Enter для выхода в меню...")

    def _show_today_tasks(self):
        """Вывод всех задач на сегодня"""
        tasks = self.controller.get_today_tasks()
        self.display_tasks(tasks)
        input("\nНажмите Enter для выхода в меню...")

    def _show_tasks_by_date(self):
        """Фильтрация задач по дате"""
        date = self.input_date("Введите дату для фильтрации (DD-MM-YYYY): ")
        tasks = self.controller.get_task_by_date(date)
        self.display_tasks(tasks)
        input("\nНажмите Enter для выхода в меню...")

    def _sort_by_priority(self):
        """Сортировка задач по приоритету с группировкой"""
        sorted_tasks = self.controller.sorted_by_priority()
        grouped = groupby(sorted_tasks, key=lambda t: t.priority.value)

        index = 1
        for priority, group in grouped:
            print(f"Приоритет: {priority}")
            for task in group:
                print(f"  {self.format_task(task, index)}")
                index += 1
            print()

        input("\nНажмите Enter для выхода в меню...")


    def format_task(self, task, index=None):
        """
        Форматирует задачу в строку для вывода

        task: объект Task
        index: номер задачи (опционально)
        return: строковое представление задачи
        """
        marker = f"[{index}] " if index is not None else ""
        return (
            f"{marker}{task.date} | {task.title} | {task.description} | "
            f"{task.category.value} | {task.priority.value} | "
            f"{'Выполнено' if task.is_done else 'Не выполнено'}"
        )

    def choose_enum(self, enum_type):
        """
        Позволяет пользователю выбрать значение из Enum

        enum_type: тип Enum (Category или Priority)
        return: выбранное значение Enum
        """
        values = list(enum_type)
        for i, item in enumerate(values, start=1):
            print(f"{i}. {item.name} ({item.value})")

        while True:
            choice = input("Введите номер: ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(values)):
                print("Неверный выбор. Попробуйте ещё раз.")
                continue
            return values[int(choice) - 1]

    def input_date(self, prompt="Введите дату (DD-MM-YYYY): "):
        """
        Запрашивает у пользователя дату и валидирует формат

        prompt: текст приглашения
        return: строка с датой
        """
        while True:
            value = input(prompt).strip()
            try:
                datetime.strptime(value, "%d-%m-%Y")
                return value
            except ValueError:
                print("Неверный формат даты. Используйте DD-MM-YYYY.")

    def display_tasks(self, tasks):
        """
        Выводит список задач

        tasks: список объектов Task
        """
        if not tasks:
            print("Задач не найдено.")
            return
        for i, task in enumerate(tasks, start=1):
            print(self.format_task(task, i))

    def _sort_by_category(self):
        """Сортировка задач по категории с группировкой"""
        sorted_tasks = self.controller.sorted_by_category()
        grouped = groupby(sorted_tasks, key=lambda t: t.category.value)

        index = 1
        for category, group in grouped:
            print(f"Категория: {category}")
            for task in group:
                print(f"  {self.format_task(task, index)}")
                index += 1
            print()

        input("\nНажмите Enter для выхода в меню...")

    def _mark_task_done(self):
        """Пометка выбранной задачи как выполненной"""
        tasks = self.controller.get_all_tasks()

        if not tasks:
            print("Нет задач для изменения статуса.")
            return

        self.display_tasks(tasks)

        idx = input("Введите номер задачи: ").strip()
        if not idx.isdigit() or not (1 <= int(idx) <= len(tasks)):
            print("Неверный индекс.")
            return

        task = tasks[int(idx) - 1]
        task.is_done = True
        self.controller.update_task_status(task)

        print("Задача помечена как выполненная.")
        input("\nНажмите Enter для выхода в меню...")

    def _delete_task(self):
        """Удаление выбранной задачи"""
        tasks = self.controller.get_all_tasks()

        if not tasks:
            print("Нет задач для удаления")
            return

        self.display_tasks(tasks)

        idx = input("Введите номер задачи: ").strip()
        if not idx.isdigit() or not (1 <= int(idx) <= len(tasks)):
            print("Неверный индекс.")
            return

        task = tasks[int(idx) - 1]
        self.controller.delete_task(task)

        print("Задача удалена")
        input("\nНажмите Enter для выхода в меню...")