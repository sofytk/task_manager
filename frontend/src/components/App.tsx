import React, { useState, useEffect } from 'react';
import { Task, FilterState } from '../types';
import { api } from '../api';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import Filter from './Filter';
import DatePicker from './DatePicker';
import '../App.css';
import plusIcon from '../components/add.png';

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string>(() => {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    return `${day}-${month}-${year}`;
  });
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState<FilterState>({
    category: 'ALL',
    priority: 'ALL',
    completion: 'ALL',
  });

  // Load tasks for selected date
  useEffect(() => {
    loadTasks();
  }, [selectedDate]);

  // Apply filters
  useEffect(() => {
    applyFilters();
  }, [tasks, filter]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTasksByDate(selectedDate);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = tasks;

    if (filter.category !== 'ALL') {
      filtered = filtered.filter((task) => task.category === filter.category);
    }

    if (filter.priority !== 'ALL') {
      filtered = filtered.filter((task) => task.priority === filter.priority);
    }

    if (filter.completion === 'DONE') {
      filtered = filtered.filter((task) => task.is_done);
    } else if (filter.completion === 'PENDING') {
      filtered = filtered.filter((task) => !task.is_done);
    }

    setFilteredTasks(filtered);
  };

  const handleAddTask = async () => {
    setShowForm(false);
    await loadTasks();
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await api.deleteTask(taskId);
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  const handleToggleTask = async (taskId: string) => {
    try {
      await api.toggleTaskCompletion(taskId);
      await loadTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const formatDateDisplay = (dateStr: string): string => {
    const [day, month, year] = dateStr.split('-');
    const date = new Date(`${year}-${month}-${day}`);
    const dayName = date.toLocaleDateString('ru-RU', { weekday: 'long' });
    const capitalizedDayName = dayName.charAt(0).toUpperCase() + dayName.slice(1);
  return `${capitalizedDayName}, ${parseInt(day)}`;
  };

  return (
    <div className="app">
      <div className="main-content">
        <div className="left-panel">
          <div className="date-header">{formatDateDisplay(selectedDate)}</div>

          <div className="controls">
            <Filter filter={filter} onFilterChange={setFilter} />
          </div>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Загрузка задач...</div>
          ) : filteredTasks.length === 0 ? (
            <div className="empty-state">
              {tasks.length === 0 ? 'Нет задач на эту дату' : 'Нет задач, соответствующих фильтрам'}
            </div>
          ) : (
            <TaskList
              tasks={filteredTasks}
              onDeleteTask={handleDeleteTask}
              onToggleTask={handleToggleTask}
            />
          )}
        </div>

        <div className="right-panel">
          <div className="calendar-panel-header">
            <button
              className="add-button add-button-wide"
              title="Добавить задачу"
              onClick={() => setShowForm(!showForm)}>
              <img 
                src={plusIcon} 
                alt="Добавить" 
                className="button-icon"
              />
              Добавить
            </button>
          </div>

          {showForm && (
            <TaskForm selectedDate={selectedDate} onTaskAdded={handleAddTask} />
          )}

          <DatePicker selectedDate={selectedDate} onDateSelect={setSelectedDate} />
        </div>
      </div>
    </div>
  );
}
