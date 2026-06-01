import { apiRequest } from "./api"
import type { Todo, TodoCreate, TodoUpdate } from "../types"

export async function createTodo(data: TodoCreate): Promise<Todo> {
  return apiRequest("/todos/", {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export async function listTodos(params?: {
  title?: string
  state?: string
  offset?: number
  limit?: number
}): Promise<Todo[]> {
  const searchParams = new URLSearchParams()
  if (params?.title) searchParams.set("title", params.title)
  if (params?.state) searchParams.set("state", params.state)
  if (params?.offset !== undefined) searchParams.set("offset", String(params.offset))
  if (params?.limit !== undefined) searchParams.set("limit", String(params.limit))

  const query = searchParams.toString()
  const data = await apiRequest<{ todos: Todo[] }>(`/todos/${query ? `?${query}` : ""}`)
  return data.todos
}

export async function updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
  return apiRequest(`/todos/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  })
}

export async function deleteTodo(id: number): Promise<void> {
  await apiRequest(`/todos/${id}`, { method: "DELETE" })
}
