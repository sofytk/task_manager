import { Task, TaskRequest } from './types';

const API_BASE_URL = 'http://192.168.31.60:8000/tasks';

export const api = {
  // Get all tasks
  getAllTasks: async (): Promise<Task[]> => {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) throw new Error('Failed to fetch tasks');
    return response.json();
  },

  // Get today's tasks
  getTodayTasks: async (): Promise<Task[]> => {
    const response = await fetch(`${API_BASE_URL}/today`);
    if (!response.ok) throw new Error('Failed to fetch today tasks');
    return response.json();
  },

  // Get tasks by date
  getTasksByDate: async (date: string): Promise<Task[]> => {
    const response = await fetch(`${API_BASE_URL}/date/${date}`);
    if (!response.ok) throw new Error('Failed to fetch tasks by date');
    return response.json();
  },

  // Create task
  createTask: async (task: TaskRequest): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });
    if (!response.ok) throw new Error('Failed to create task');
    return response.json();
  },

  // Delete task
  deleteTask: async (taskId: string): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/${taskId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete task');
  },

  // Toggle task completion
  toggleTaskCompletion: async (taskId: string): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/${taskId}/toggle`, {
      method: 'PATCH',
    });
    if (!response.ok) throw new Error('Failed to toggle task');
    return response.json();
  },

  // Sort tasks
  sortTasks: async (field: 'priority' | 'date' | 'category' | 'title'): Promise<Task[]> => {
    const response = await fetch(`${API_BASE_URL}/sort/${field}`);
    if (!response.ok) throw new Error('Failed to sort tasks');
    return response.json();
  },

  // Update task
  updateTask: async (taskId: string, task: TaskRequest): Promise<Task> => {
    const response = await fetch(`${API_BASE_URL}/${taskId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });
    if (!response.ok) throw new Error('Failed to update task');
    return response.json();
  },
};
