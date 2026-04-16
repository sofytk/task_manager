# test/task_repository_test.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import mock_open, patch, MagicMock
import json
import tempfile
import shutil

from data.task_repository import TaskRepository
from domain.model.task import Task
from domain.model.priority import Priority
from domain.model.category import Category


class TestTaskRepository(unittest.TestCase):
    """Тесты для TaskRepository с моками"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_tasks_data = [
            {
                "id": "test-id-1",
                "title": "Тестовая задача 1",
                "description": "Описание 1",
                "date": "01-01-2024",
                "priority": "HIGH",
                "category": "WORK",
                "is_done": False
            },
            {
                "id": "test-id-2",
                "title": "Тестовая задача 2",
                "description": "Описание 2",
                "date": "15-02-2024",
                "priority": "MEDIUM",
                "category": "FAMILY",
                "is_done": True
            },
            {
                "id": "test-id-3",
                "title": "Тестовая задача 3",
                "description": "Описание 3",
                "date": "01-01-2024",
                "priority": "LOW",
                "category": "HOBBIES",
                "is_done": False
            }
        ]
        
        self.test_task = Task(
            id="new-test-id",
            date="20-03-2024",
            title="Новая задача",
            description="Описание новой задачи",
            priority=Priority.MEDIUM,
            is_done=False,
            category=Category.WORK
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_all_tasks_success(self, mock_json_load, mock_file):
        """Тест: успешное получение всех задач"""
        mock_json_load.return_value = self.test_tasks_data
        
        repo = TaskRepository()
        tasks = repo.get_all_tasks()
        
        self.assertEqual(len(tasks), 3)
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(tasks[0].id, "test-id-1")
        self.assertEqual(tasks[0].title, "Тестовая задача 1")
        self.assertEqual(tasks[1].priority, Priority.MEDIUM)
        self.assertEqual(tasks[2].category, Category.HOBBIES)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_all_tasks_empty_file(self, mock_json_load, mock_file):
        """Тест: получение задач из пустого файла"""
        mock_json_load.return_value = []
        
        repo = TaskRepository()
        tasks = repo.get_all_tasks()
        
        self.assertEqual(tasks, [])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_all_tasks_with_invalid_data(self, mock_json_load, mock_file):
        """Тест: обработка некорректных данных"""
        invalid_data = [
            self.test_tasks_data[0],
            {"invalid": "data"},
            self.test_tasks_data[1]
        ]
        mock_json_load.return_value = invalid_data
        
        repo = TaskRepository()
        tasks = repo.get_all_tasks()
        
        self.assertEqual(len(tasks), 2)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_tasks_by_date(self, mock_json_load, mock_file):
        """Тест: получение задач по дате"""
        mock_json_load.return_value = self.test_tasks_data
        
        repo = TaskRepository()
        tasks = repo.get_tasks_by_date("01-01-2024")
        
        self.assertEqual(len(tasks), 2)
        for task in tasks:
            self.assertEqual(task.date, "01-01-2024")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_tasks_by_date_no_matches(self, mock_json_load, mock_file):
        """Тест: нет задач на дату"""
        mock_json_load.return_value = self.test_tasks_data
        
        repo = TaskRepository()
        tasks = repo.get_tasks_by_date("99-99-9999")
        
        self.assertEqual(tasks, [])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_add_task_success(self, mock_json_dump, mock_json_load, mock_file):
        """Тест: успешное добавление задачи"""
        mock_json_load.return_value = self.test_tasks_data.copy()
        
        repo = TaskRepository()
        repo.add_task(self.test_task)
        
        mock_json_dump.assert_called_once()
        call_args = mock_json_dump.call_args[0]
        updated_data = call_args[0]
        
        self.assertEqual(len(updated_data), 4)
        self.assertEqual(updated_data[-1]["id"], "new-test-id")
        self.assertEqual(updated_data[-1]["title"], "Новая задача")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_delete_task_success(self, mock_json_dump, mock_json_load, mock_file):
        """Тест: успешное удаление задачи"""
        mock_json_load.return_value = self.test_tasks_data.copy()
        
        task_to_delete = Task(
            id="test-id-1",
            date="01-01-2024",
            title="Тестовая задача 1",
            description="Описание 1",
            priority=Priority.HIGH,
            is_done=False,
            category=Category.WORK
        )
        
        repo = TaskRepository()
        repo.delete_task(task_to_delete)
        
        call_args = mock_json_dump.call_args[0]
        updated_data = call_args[0]
        
        self.assertEqual(len(updated_data), 2)
        self.assertTrue(all(t["id"] != "test-id-1" for t in updated_data))

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_delete_task_not_found(self, mock_json_dump, mock_json_load, mock_file):
        """Тест: удаление несуществующей задачи"""
        mock_json_load.return_value = self.test_tasks_data.copy()
        
        task_to_delete = Task(
            id="non-existent-id",
            date="01-01-2024",
            title="Несуществующая задача",
            description="Описание",
            priority=Priority.LOW,
            is_done=False,
            category=Category.HEALTH
        )
        
        repo = TaskRepository()
        repo.delete_task(task_to_delete)
        
        call_args = mock_json_dump.call_args[0]
        updated_data = call_args[0]
        self.assertEqual(len(updated_data), 3)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_task_success(self, mock_json_dump, mock_json_load, mock_file):
        """Тест: успешное обновление задачи"""
        mock_json_load.return_value = self.test_tasks_data.copy()
        
        updated_task = Task(
            id="test-id-1",
            date="01-01-2024",
            title="ОБНОВЛЕННАЯ задача",
            description="Новое описание",
            priority=Priority.LOW,
            is_done=True,
            category=Category.HEALTH
        )
        
        repo = TaskRepository()
        result = repo.update_data(updated_task)
        
        call_args = mock_json_dump.call_args[0]
        updated_data = call_args[0]
        
        updated_entry = next(t for t in updated_data if t["id"] == "test-id-1")
        self.assertEqual(updated_entry["title"], "ОБНОВЛЕННАЯ задача")
        self.assertEqual(updated_entry["priority"], "LOW")
        self.assertEqual(updated_entry["is_done"], True)
        
        self.assertEqual(result, updated_task)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_task_not_found(self, mock_json_dump, mock_json_load, mock_file):
        """Тест: обновление несуществующей задачи"""
        mock_json_load.return_value = self.test_tasks_data.copy()
        
        non_existent_task = Task(
            id="non-existent-id",
            date="01-01-2024",
            title="Несуществующая задача",
            description="Описание",
            priority=Priority.LOW,
            is_done=False,
            category=Category.HEALTH
        )
        
        repo = TaskRepository()
        
        with self.assertRaises(ValueError) as context:
            repo.update_data(non_existent_task)
        
        self.assertEqual(str(context.exception), 'Task to update not found')
        mock_json_dump.assert_not_called()


class TestTaskRepositoryIntegration(unittest.TestCase):
    """Интеграционные тесты с временным файлом"""
    
    def setUp(self):
        """Создание временного файла с валидными данными"""
        # Создаем временную директорию
        self.temp_dir = tempfile.mkdtemp()
        self.temp_db_path = os.path.join(self.temp_dir, "test_tasks.json")
        
        # Сохраняем оригинальный путь
        self.original_db_name = TaskRepository.DATABASE_NAME
        
        # Создаем валидный JSON файл с пустым массивом
        with open(self.temp_db_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        # Подменяем путь к БД
        TaskRepository.DATABASE_NAME = self.temp_db_path
        
        # Создаем тестовые задачи
        self.test_tasks = [
            Task(
                id="int-test-1",
                date="01-01-2024",
                title="Интеграционная задача 1",
                description="Описание 1",
                priority=Priority.HIGH,
                is_done=False,
                category=Category.WORK
            ),
            Task(
                id="int-test-2",
                date="15-02-2024",
                title="Интеграционная задача 2",
                description="Описание 2",
                priority=Priority.MEDIUM,
                is_done=True,
                category=Category.FAMILY
            )
        ]
        
        # Создаем репозиторий и добавляем задачи
        self.repo = TaskRepository()
        for task in self.test_tasks:
            self.repo.add_task(task)
    
    def tearDown(self):
        """Очистка временного файла и директории"""
        # Восстанавливаем оригинальный путь
        TaskRepository.DATABASE_NAME = self.original_db_name
        
        # Удаляем временную директорию
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_integration_get_all_tasks(self):
        """Интеграционный тест: получение всех задач"""
        tasks = self.repo.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, "int-test-1")
        self.assertEqual(tasks[1].id, "int-test-2")
        self.assertEqual(tasks[0].title, "Интеграционная задача 1")
        self.assertEqual(tasks[1].priority, Priority.MEDIUM)
    
    def test_integration_add_and_get(self):
        """Интеграционный тест: добавление и получение задачи"""
        new_task = Task(
            id=None,  # ID должен сгенерироваться автоматически
            date="20-03-2024",
            title="Новая интеграционная задача",
            description="Описание",
            priority=Priority.LOW,
            is_done=False,
            category=Category.HOBBIES
        )
        
        self.repo.add_task(new_task)
        tasks = self.repo.get_all_tasks()
        
        self.assertEqual(len(tasks), 3)
        # Проверяем, что ID сгенерировался
        self.assertIsNotNone(tasks[2].id)
        self.assertNotEqual(tasks[2].id, "")
        self.assertEqual(tasks[2].title, "Новая интеграционная задача")
        self.assertEqual(tasks[2].priority, Priority.LOW)
        self.assertEqual(tasks[2].category, Category.HOBBIES)
    
    def test_integration_update_task(self):
        """Интеграционный тест: обновление задачи"""
        updated_task = Task(
            id="int-test-1",
            date="01-01-2024",
            title="ОБНОВЛЕННАЯ интеграционная задача",
            description="Новое описание",
            priority=Priority.LOW,
            is_done=True,
            category=Category.HEALTH
        )
        
        result = self.repo.update_data(updated_task)
        
        # Проверяем результат
        self.assertEqual(result.title, "ОБНОВЛЕННАЯ интеграционная задача")
        
        # Проверяем, что данные сохранились
        tasks = self.repo.get_all_tasks()
        updated = next(t for t in tasks if t.id == "int-test-1")
        self.assertEqual(updated.title, "ОБНОВЛЕННАЯ интеграционная задача")
        self.assertEqual(updated.description, "Новое описание")
        self.assertEqual(updated.priority, Priority.LOW)
        self.assertTrue(updated.is_done)
        self.assertEqual(updated.category, Category.HEALTH)
    
    def test_integration_delete_task(self):
        """Интеграционный тест: удаление задачи"""
        task_to_delete = Task(
            id="int-test-1",
            date="01-01-2024",
            title="Интеграционная задача 1",
            description="Описание 1",
            priority=Priority.HIGH,
            is_done=False,
            category=Category.WORK
        )
        
        self.repo.delete_task(task_to_delete)
        tasks = self.repo.get_all_tasks()
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, "int-test-2")
    
    def test_integration_get_by_date(self):
        """Интеграционный тест: получение задач по дате"""
        tasks = self.repo.get_tasks_by_date("01-01-2024")
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, "int-test-1")
        self.assertEqual(tasks[0].date, "01-01-2024")


if __name__ == '__main__':
    unittest.main()