export interface User {
  id: number
  username: string
  email: string
}

export type TodoState = "draft" | "todo" | "doing" | "done" | "trash"

export interface Todo {
  id: number
  title: string
  description: string
  state: TodoState
}

export interface TodoCreate {
  title: string
  description: string
  state: TodoState
}

export interface TodoUpdate {
  title?: string
  description?: string
  state?: TodoState
}
