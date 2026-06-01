"use client"

import { useState } from "react"
import { ProtectedRoute } from "../../components/ProtectedRoute"
import { useTodos } from "../../hooks/useTodos"
import type { TodoState, TodoCreate } from "../../types"

const STATE_LABELS: Record<TodoState, string> = {
  draft: "Rascunho",
  todo: "A Fazer",
  doing: "Fazendo",
  done: "Concluído",
  trash: "Lixo",
}

const STATE_COLORS: Record<TodoState, string> = {
  draft: "bg-slate-500/20 text-slate-400",
  todo: "bg-blue-500/20 text-blue-400",
  doing: "bg-yellow-500/20 text-yellow-400",
  done: "bg-green-500/20 text-green-400",
  trash: "bg-red-500/20 text-red-400",
}

const TODO_STATES: TodoState[] = ["draft", "todo", "doing", "done", "trash"]

export default function Dashboard() {
  return (
    <ProtectedRoute>
      <TodoDashboard />
    </ProtectedRoute>
  )
}

function TodoDashboard() {
  const { todos, loading, error, stateFilter, setStateFilter, addTodo, editTodo, removeTodo } =
    useTodos()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState<TodoCreate>({ title: "", description: "", state: "todo" })
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    try {
      await addTodo(form)
      setForm({ title: "", description: "", state: "todo" })
      setShowForm(false)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Minhas Tarefas</h1>
          <p className="mt-1 text-slate-400">
            {todos.length} {todos.length === 1 ? "tarefa" : "tarefas"}
          </p>
        </div>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="rounded-xl bg-blue-600 px-5 py-2.5 font-semibold transition hover:bg-blue-700"
        >
          + Nova tarefa
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="mb-8 space-y-4 rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >
          <h2 className="text-lg font-semibold">Nova tarefa</h2>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-slate-300">Título</label>
            <input
              type="text"
              value={form.title}
              onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              required
              placeholder="Título da tarefa"
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-white placeholder-slate-500 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-slate-300">Descrição</label>
            <textarea
              value={form.description}
              onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
              required
              placeholder="Descreva a tarefa..."
              rows={3}
              className="w-full resize-none rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-white placeholder-slate-500 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-slate-300">Estado</label>
            <select
              value={form.state}
              onChange={(e) => setForm((f) => ({ ...f, state: e.target.value as TodoState }))}
              className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-white outline-none focus:border-blue-500"
            >
              {TODO_STATES.map((s) => (
                <option key={s} value={s}>
                  {STATE_LABELS[s]}
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-3 pt-1">
            <button
              type="submit"
              disabled={submitting}
              className="rounded-lg bg-blue-600 px-5 py-2 font-semibold transition hover:bg-blue-700 disabled:opacity-70"
            >
              {submitting ? "Salvando..." : "Salvar"}
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="rounded-lg border border-slate-700 px-5 py-2 text-slate-300 transition hover:bg-slate-800"
            >
              Cancelar
            </button>
          </div>
        </form>
      )}

      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setStateFilter("")}
          className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
            stateFilter === ""
              ? "bg-blue-600 text-white"
              : "bg-slate-800 text-slate-400 hover:bg-slate-700"
          }`}
        >
          Todas
        </button>
        {TODO_STATES.map((s) => (
          <button
            key={s}
            onClick={() => setStateFilter(s)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
              stateFilter === s
                ? "bg-blue-600 text-white"
                : "bg-slate-800 text-slate-400 hover:bg-slate-700"
            }`}
          >
            {STATE_LABELS[s]}
          </button>
        ))}
      </div>

      {error && (
        <div className="mb-6 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-20">
          <p className="text-slate-500">Carregando...</p>
        </div>
      ) : todos.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800 bg-slate-900 py-20 text-center">
          <p className="text-lg text-slate-500">Nenhuma tarefa encontrada</p>
          <p className="mt-1 text-sm text-slate-600">Clique em &quot;+ Nova tarefa&quot; para começar</p>
        </div>
      ) : (
        <ul className="space-y-3">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className="flex items-start justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900 p-5"
            >
              <div className="min-w-0 flex-1">
                <div className="mb-1 flex items-center gap-3">
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${STATE_COLORS[todo.state]}`}
                  >
                    {STATE_LABELS[todo.state]}
                  </span>
                  <h3 className="truncate font-semibold">{todo.title}</h3>
                </div>
                <p className="line-clamp-2 text-sm text-slate-400">{todo.description}</p>
              </div>

              <div className="flex shrink-0 items-center gap-2">
                <select
                  value={todo.state}
                  onChange={(e) => editTodo(todo.id, { state: e.target.value as TodoState })}
                  className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-300 outline-none focus:border-blue-500"
                >
                  {TODO_STATES.map((s) => (
                    <option key={s} value={s}>
                      {STATE_LABELS[s]}
                    </option>
                  ))}
                </select>
                <button
                  onClick={() => removeTodo(todo.id)}
                  className="rounded-lg border border-slate-700 px-3 py-1.5 text-sm text-red-400 transition hover:border-red-500/30 hover:bg-red-500/10"
                >
                  Excluir
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
