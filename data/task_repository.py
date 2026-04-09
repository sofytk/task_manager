import json
from data.base_task_repository import BaseTaskRepository
from domain.model.task import Task


class TaskRepository(BaseTaskRepository):
    """
    Реализация репозитория задач.

    Отвечает за хранение и извлечение задач из JSON-файла.
    """

    DATABASE_NAME = "data/tasks_database.json"

    def get_all_tasks(self):
        """
        Получить все задачи из хранилища.

        return: список объектов Task
        """
        raw = self.__read_database()
        tasks = []

        for item in raw:
            try:
                tasks.append(Task.from_dict(item))
            except Exception:
                continue

        return tasks

    def get_tasks_by_date(self, date):
        """
        Получить задачи по заданной дате.

        date: дата в формате строки (DD-MM-YYYY)
        return: список задач
        """
        return [task for task in self.get_all_tasks() if task.date == date]

    def add_task(self, task):
        """
        Добавить новую задачу в хранилище.

        task: объект Task
        """
        tasks = self.__read_database()
        tasks.append(task.to_dict())
        self.__write_database(tasks)

    def delete_task(self, task):
        """
        Удалить задачу

        task: объект Task, который удаляем
        """
        tasks = self.__read_database()
        tasks = [t for t in tasks if t.get('id') != task.id]
        self.__write_database(tasks)
        

    def update_data(self, task):
        """
        Обновить существующую задачу.

        Задача ищется по совпадению даты и названия.

        task: объект Task с обновлёнными данными
        return: обновлённый объект Task
        """
        tasks = self.__read_database()
        updated = False

        for i, item in enumerate(tasks):
            if item.get('id') == task.id:
                tasks[i] = task.to_dict()
                updated = True
                break


        if not updated:
            raise ValueError('Task to update not found')

        self.__write_database(tasks)
        return task

    def __read_database(self):
        """
        Прочитать данные из JSON-файла.

        return: список словарей с задачами
        """
        with open(TaskRepository.DATABASE_NAME, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def __write_database(self, data):
        """
        Записать данные в JSON-файл.

        data: список словарей задач
        """
        with open(TaskRepository.DATABASE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)