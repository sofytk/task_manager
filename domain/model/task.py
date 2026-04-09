from domain.model.category import Category
from domain.model.priority import Priority
import uuid


class Task:
    def __init__(self, date, title, description, priority, is_done, category):
        self._id = id if id else str(uuid.uuid4())
        self._date = date
        self._title = title
        self._description = description
        self._priority = priority
        self._is_done = is_done
        self._category = category

    @property
    def id(self):
        return self._id
    
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def is_done(self):
        return self._is_done

    @is_done.setter
    def is_done(self, value):
        self._is_done = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "priority": self.priority.name,
            "category": self.category.name,
            "is_done": self.is_done
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["date"],
            data["title"],
            data["description"],
            Priority[data["priority"]],
            data["is_done"],
            Category[data["category"]]
        )