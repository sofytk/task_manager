import React, { useRef } from 'react';
import { Task } from '../types';

interface TaskItemProps {
  task: Task;
  onDelete: () => void;
  onToggle: () => void;
}

const CATEGORY_LABELS: Record<string, string> = {
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

export default function TaskItem({ task, onDelete, onToggle }: TaskItemProps) {
  const contextMenuRef = useRef<HTMLDivElement>(null);
  const [showContextMenu, setShowContextMenu] = React.useState(false);
  const [contextMenuPos, setContextMenuPos] = React.useState({ x: 0, y: 0 });
  const [showDescription, setShowDescription] = React.useState(false);
  const getPriorityColor = (priority: string): string => {
    switch (priority) {
      case 'HIGH':
        return '#FF6666'; // red
      case 'MEDIUM':
        return '#FFFD8F'; // yellow
      case 'LOW':
        return '#68FF66'; // green
      default:
        return '#9ca3af'; // gray
    }
  };

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setContextMenuPos({ x: e.clientX, y: e.clientY });
    setShowContextMenu(true);
  };

  const handleDeleteClick = () => {
    setShowContextMenu(false);
    onDelete();
  };

  const handleToggleDescription = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('input[type="checkbox"]')) {
      return;
    }
    setShowDescription((prev) => !prev);
  };

  // Close context menu when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (contextMenuRef.current && !contextMenuRef.current.contains(e.target as Node)) {
        setShowContextMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <>
      <div
        className={`task-item ${task.is_done ? 'completed' : ''}`}
        onContextMenu={handleContextMenu}
        onClick={handleToggleDescription}
      >
        <div
          className="priority-indicator"
          style={{ backgroundColor: getPriorityColor(task.priority),
            transform: 'rotate(180deg)',
           }}
        />
        <div className="task-content">
          <div className="task-title">{task.title}</div>
          <div className="task-category">{CATEGORY_LABELS[task.category] || task.category}</div>
        </div>
        <input
          type="checkbox"
          checked={task.is_done}
          onChange={(e) => {
            e.stopPropagation();
            onToggle();
          }}
          className="task-checkbox"
          title="Отметить как выполненное"
        />
      </div>

      {showDescription && task.description && (
        <div className="task-description">
          Описание: <span className="description-text">{task.description}</span>
        </div>
      )}

      {showContextMenu && (
        <div
          ref={contextMenuRef}
          className="context-menu"
          style={{ top: `${contextMenuPos.y}px`, left: `${contextMenuPos.x}px` }}
        >
          <button className="context-menu-item delete" onClick={handleDeleteClick}>
            Удалить
          </button>
        </div>
      )}
    </>
  );
}
