"use client"

import { useEffect, useState } from "react"
import { getUsers } from "../../services/api"
import type { User } from "../../types"

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getUsers()
      .then(setUsers)
      .catch(() => setError("Erro ao carregar usuários"))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Usuários</h1>
        {!loading && !error && (
          <p className="mt-1 text-slate-400">
            {users.length} {users.length === 1 ? "usuário" : "usuários"} cadastrados
          </p>
        )}
      </div>

      {error && (
        <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-20">
          <p className="text-slate-500">Carregando...</p>
        </div>
      ) : users.length === 0 ? (
        <div className="rounded-2xl border border-slate-800 bg-slate-900 py-20 text-center">
          <p className="text-slate-500">Nenhum usuário encontrado</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800">
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  ID
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Usuário
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                  Email
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {users.map((user) => (
                <tr key={user.id} className="transition hover:bg-slate-800/50">
                  <td className="px-6 py-4 text-sm text-slate-400">#{user.id}</td>
                  <td className="px-6 py-4 font-medium">{user.username}</td>
                  <td className="px-6 py-4 text-sm text-slate-400">{user.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  )
}
