from data.task_repository import TaskRepository
from datetime import date


class TaskController:
    """
    Класс бизнес-логики для управления задачами

    Отвечает за обработку задач, их фильтрацию, сортировку
    и взаимодействие с репозиторием данных.
    """

    def __init__(self):
        """
        Инициализация контроллера и подключение репозитория
        """
        self.repository = TaskRepository()

    def get_all_tasks(self):
        """
        Получить список всех задач

        return: список объектов Task
        """
        return self.repository.get_all_tasks()

    def get_task_by_date(self, current_date):
        """
        Получить задачи по заданной дате

        current_date: дата в формате строки (DD-MM-YYYY)
        return: список задач
        """
        return self.repository.get_tasks_by_date(current_date)

    def get_today_tasks(self):
        """
        Получить задачи на текущую дату

        return: список задач на сегодня
        """
        today_tasks = self.repository.get_tasks_by_date(date.today().strftime("%d-%m-%Y"))
        return today_tasks

    def add_task(self, task):
        """
        Добавить новую задачу

        task: объект Task
        """
        self.repository.add_task(task)

    def delete_task(self, task):
        """
        Удалить задачу

        task: объект Task
        """
        self.repository.delete_task(task)

    def update_task_status(self, task):
        """
        Обновить статус задачи (пометить как выполненную)

        task: объект Task
        """
        task.is_done = True
        self.repository.update_data(task)

    def sorted_by_priority(self):
        """
        Получить список задач, отсортированных по приоритету

        return: отсортированный список задач
        """
        task_list = self.get_all_tasks()
        return sorted(task_list, key=lambda task: task.priority.value)

    def sorted_by_category(self):
        """
        Получить список задач, отсортированных по категории

        return: отсортированный список задач
        """
        task_list = self.get_all_tasks()
        return sorted(task_list, key=lambda task: task.category.value)