"use client"

import { useState, useEffect, useCallback } from "react"
import { createTodo, listTodos, updateTodo, deleteTodo } from "../services/todo"
import type { Todo, TodoCreate, TodoUpdate, TodoState } from "../types"

export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [stateFilter, setStateFilter] = useState<TodoState | "">("")

  const fetchTodos = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await listTodos(stateFilter ? { state: stateFilter } : undefined)
      setTodos(data)
    } catch {
      setError("Erro ao carregar tarefas")
    } finally {
      setLoading(false)
    }
  }, [stateFilter])

  useEffect(() => {
    fetchTodos()
  }, [fetchTodos])

  async function addTodo(data: TodoCreate) {
    const todo = await createTodo(data)
    setTodos((prev) => [todo, ...prev])
  }

  async function editTodo(id: number, data: TodoUpdate) {
    const updated = await updateTodo(id, data)
    setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)))
  }

  async function removeTodo(id: number) {
    await deleteTodo(id)
    setTodos((prev) => prev.filter((t) => t.id !== id))
  }

  return {
    todos,
    loading,
    error,
    stateFilter,
    setStateFilter,
    addTodo,
    editTodo,
    removeTodo,
    refetch: fetchTodos,
  }
}
