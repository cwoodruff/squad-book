export type TaskStatus = 'todo' | 'doing' | 'done';

export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  createdAt: string;
}

export class TaskStore {
  private tasks = new Map<number, Task>();
  private nextId = 1;

  list(): Task[] {
    return [...this.tasks.values()];
  }

  get(id: number): Task | undefined {
    return this.tasks.get(id);
  }

  create(title: string): Task {
    if (!title || !title.trim()) throw new Error('title is required');
    const task: Task = { id: this.nextId++, title: title.trim(), status: 'todo', createdAt: new Date().toISOString() };
    this.tasks.set(task.id, task);
    return task;
  }

  setStatus(id: number, status: TaskStatus): Task | undefined {
    const task = this.tasks.get(id);
    if (!task) return undefined;
    task.status = status;
    return task;
  }

  remove(id: number): boolean {
    return this.tasks.delete(id);
  }
}
