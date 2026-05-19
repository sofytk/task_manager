export interface Task {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  date: string;
  is_done: boolean;
}

export interface TaskRequest {
  title: string;
  description?: string;
  category: string;
  priority: string;
  date: string;
}

export type Priority = 'HIGH' | 'MEDIUM' | 'LOW';
export type Category = 
  | 'WORK'
  | 'HOME'
  | 'FAMILY'
  | 'HEALTH'
  | 'LEARNING'
  | 'FINANCES'
  | 'HOBBIES'
  | 'SELF_DEVELOPMENT'
  | 'ENTERTAINMENT';

export interface FilterState {
  category: Category | 'ALL';
  priority: Priority | 'ALL';
  completion: 'ALL' | 'DONE' | 'PENDING';
}
