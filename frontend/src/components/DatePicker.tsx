import React from 'react';

interface DatePickerProps {
  selectedDate: string;
  onDateSelect: (date: string) => void;
}

export default function DatePicker({ selectedDate, onDateSelect }: DatePickerProps) {
  const [currentMonth, setCurrentMonth] = React.useState<Date>(() => {
    const [day, month, year] = selectedDate.split('-').map(Number);
    return new Date(year, month - 1, day);
  });

  const getDaysInMonth = (date: Date): number => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date: Date): number => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const formatDate = (day: number, month: number, year: number): string => {
    return `${String(day).padStart(2, '0')}-${String(month + 1).padStart(2, '0')}-${year}`;
  };

  const handlePrevMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 1));
  };

  const handleDateClick = (day: number) => {
    const date = formatDate(day, currentMonth.getMonth(), currentMonth.getFullYear());
    onDateSelect(date);
  };

  const isDateSelected = (day: number): boolean => {
    const [selDay, selMonth, selYear] = selectedDate.split('-').map(Number);
    return (
      day === selDay &&
      currentMonth.getMonth() === selMonth - 1 &&
      currentMonth.getFullYear() === selYear
    );
  };

  const monthName = currentMonth.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' });
  const daysInMonth = getDaysInMonth(currentMonth);
  const firstDay = getFirstDayOfMonth(currentMonth);
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);
  const emptyDays = Array.from({ length: firstDay }, (_, i) => i);

  return (
    <div className="date-picker">
      <div className="date-picker-header">
        <button onClick={handlePrevMonth} className="nav-button">&lt;</button>
        <span className="month-year">{monthName}</span>
        <button onClick={handleNextMonth} className="nav-button">&gt;</button>
      </div>

      <div className="weekdays">
        {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
          <div key={day} className="weekday">
            {day}
          </div>
        ))}
      </div>

      <div className="calendar-grid">
        {emptyDays.map((i) => (
          <div key={`empty-${i}`} className="calendar-day empty" />
        ))}
        {days.map((day) => (
          <button
            key={day}
            className={`calendar-day ${isDateSelected(day) ? 'selected' : ''}`}
            onClick={() => handleDateClick(day)}
          >
            {day}
          </button>
        ))}
      </div>
    </div>
  );
}
