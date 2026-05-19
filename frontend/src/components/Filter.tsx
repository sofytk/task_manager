import React from 'react';
import { FilterState, Priority, Category } from '../types';
import filterIcon from '../components/filter.png';

interface FilterProps {
  filter: FilterState;
  onFilterChange: (filter: FilterState) => void;
}

const PRIORITIES: (Priority | 'ALL')[] = ['ALL', 'HIGH', 'MEDIUM', 'LOW'];
const CATEGORIES: (Category | 'ALL')[] = [
  'ALL',
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
const COMPLETION_OPTIONS = ['ALL', 'PENDING', 'DONE'] as const;

const CATEGORY_LABELS: Record<Category | 'ALL', string> = {
  ALL: 'Все категории',
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

const PRIORITY_LABELS: Record<Priority | 'ALL', string> = {
  ALL: 'Все приоритеты',
  HIGH: 'Высокий',
  MEDIUM: 'Средний',
  LOW: 'Низкий',
};

const STATUS_LABELS: Record<'ALL' | 'DONE' | 'PENDING', string> = {
  ALL: 'Все задачи',
  DONE: 'Выполненные',
  PENDING: 'В ожидании',
};

export default function Filter({ filter, onFilterChange }: FilterProps) {
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleCategoryChange = (category: Category | 'ALL') => {
    onFilterChange({ ...filter, category });
  };

  const handlePriorityChange = (priority: Priority | 'ALL') => {
    onFilterChange({ ...filter, priority });
  };

  const handleCompletionChange = (completion: 'ALL' | 'DONE' | 'PENDING') => {
    onFilterChange({ ...filter, completion });
  };

  const getFilterLabel = (): string => {
    const labels: string[] = [];
    if (filter.category !== 'ALL') labels.push(CATEGORY_LABELS[filter.category]);
    if (filter.priority !== 'ALL') labels.push(PRIORITY_LABELS[filter.priority]);
    if (filter.completion !== 'ALL') labels.push(STATUS_LABELS[filter.completion]);
    return labels.length === 0 ? 'Фильтр' : `Фильтр (${labels.length})`;
  };

  return (
    <div className="filter-container" ref={dropdownRef}>
      <button className="filter-button" onClick={() => setIsOpen(!isOpen)}>
        <span className="filter-button-icon">
          <img src={filterIcon} alt="filter" />
        </span>
        {getFilterLabel()}
      </button>

      {isOpen && (
        <div className="filter-dropdown">
          <div className="filter-group">
            <label className="filter-label">Категория</label>
            <select
              value={filter.category}
              onChange={(e) => handleCategoryChange(e.target.value as Category | 'ALL')}
              className="filter-select"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {CATEGORY_LABELS[cat]}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">Приоритет</label>
            <select
              value={filter.priority}
              onChange={(e) => handlePriorityChange(e.target.value as Priority | 'ALL')}
              className="filter-select"
            >
              {PRIORITIES.map((pri) => (
                <option key={pri} value={pri}>
                  {PRIORITY_LABELS[pri]}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">Статус</label>
            <select
              value={filter.completion}
              onChange={(e) => handleCompletionChange(e.target.value as 'ALL' | 'DONE' | 'PENDING')}
              className="filter-select"
            >
              {COMPLETION_OPTIONS.map((opt) => (
                <option key={opt} value={opt}>
                  {STATUS_LABELS[opt]}
                </option>
              ))}
            </select>
          </div>

          <button
            className="filter-reset"
            onClick={() => onFilterChange({ category: 'ALL', priority: 'ALL', completion: 'ALL' })}
          >
            Сбросить фильтр
          </button>
        </div>
      )}
    </div>
  );
}
