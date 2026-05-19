import React, { useState } from 'react';
import { Category, Priority } from '../types';
import { api } from '../api';

interface TaskFormProps {
  selectedDate: string;
  onTaskAdded: () => void;
}

const PRIORITIES: Priority[] = ['HIGH', 'MEDIUM', 'LOW'];
const CATEGORIES: Category[] = [
  'WORK',
  'HOME',
  'FAMILY',
  'HEALTH',
  'LEARNING',
  'FINANCES',
  'HOBBIES',
  'SELF_DEVELOPMENT',
  'ENTERTAINMENT',
];

const CATEGORY_LABELS: Record<Category, string> = {
  WORK: 'Работа',
  HOME: 'Дом',
  FAMILY: 'Семья',
  HEALTH: 'Здоровье',
  LEARNING: 'Обучение',
  FINANCES: 'Финансы',
  HOBBIES: 'Хобби',
  SELF_DEVELOPMENT: 'Саморазвитие',
  ENTERTAINMENT: 'Развлечения',
};

const PRIORITY_LABELS: Record<Priority, string> = {
  HIGH: 'Высокий',
  MEDIUM: 'Средний',
  LOW: 'Низкий',
};

export default function TaskForm({ selectedDate, onTaskAdded }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState<Category>('WORK');
  const [priority, setPriority] = useState<Priority>('MEDIUM');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Введите название задачи');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await api.createTask({
        title: title.trim(),
        description: description.trim(),
        category,
        priority,
        date: selectedDate,
      });

      setTitle('');
      setDescription('');
      setCategory('WORK');
      setPriority('MEDIUM');
      onTaskAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <input
          type="text"
          placeholder="Название задачи..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="form-input"
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <textarea
          placeholder="Описание задачи..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="form-input form-textarea"
          rows={3}
          disabled={loading}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as Category)}
            className="form-select"
            disabled={loading}
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {CATEGORY_LABELS[cat]}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as Priority)}
            className="form-select"
            disabled={loading}
          >
            {PRIORITIES.map((pri) => (
              <option key={pri} value={pri}>
                {pri}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && <div className="form-error">{error}</div>}

      <button type="submit" className="form-submit" disabled={loading}>
        {loading ? 'Добавление...' : 'Добавить задачу'}
      </button>
    </form>
  );
}
