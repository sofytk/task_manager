from abc import ABC, abstractmethod
from typing import List
from domain.model.task import Task


class BaseTaskRepository(ABC):
    """
    Абстрактный базовый класс репозитория задач

    Определяет интерфейс для работы с хранилищем задач
    (получение, добавление, обновление, удаление)
    """
    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """
        Получить список всех задач

        return: список объектов Task
        """
        pass

    @abstractmethod
    def get_tasks_by_date(self, date) -> List[Task]:
        """
        Получить список задач по заданной дате

        date: дата в строковом формате (например, 'DD-MM-YYYY')
        return: список объектов Task, соответствующих дате
        """
        pass

    @abstractmethod
    def add_task(self, task) -> None:
        """
        Добавить новую задачу

        task: объект Task, который нужно сохранить
        """
        pass

    @abstractmethod
    def update_data(self, task) -> Task:
        """
        Обновить существующую задачу

        task: объект Task с обновлёнными данными
        return: обновлённый объект Task
        """
        pass

    @abstractmethod
    def delete_task(self, task) -> None:
        """
        Удалить задачу

        task: объект Task, который удаляем
        """
        pass