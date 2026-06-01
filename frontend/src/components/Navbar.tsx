"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { useAuth } from "../context/AuthContext"
import { logout } from "../services/auth"

export function Navbar() {
  const { isAuthenticated, logout: contextLogout } = useAuth()
  const router = useRouter()

  function handleLogout() {
    logout()
    contextLogout()
    router.push("/login")
  }

  return (
    <nav className="border-b border-slate-800 bg-slate-900">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-bold text-white">
          FastAPI<span className="text-blue-400">Zero</span>
        </Link>

        <div className="flex items-center gap-6">
          {isAuthenticated ? (
            <>
              <Link
                href="/dashboard"
                className="text-sm text-slate-400 transition hover:text-white"
              >
                Tarefas
              </Link>
              <Link
                href="/users"
                className="text-sm text-slate-400 transition hover:text-white"
              >
                Usuários
              </Link>
              <button
                onClick={handleLogout}
                className="rounded-lg border border-slate-700 px-4 py-1.5 text-sm text-slate-300 transition hover:bg-slate-800"
              >
                Sair
              </button>
            </>
          ) : (
            <>
              <Link
                href="/users"
                className="text-sm text-slate-400 transition hover:text-white"
              >
                Usuários
              </Link>
              <Link
                href="/login"
                className="rounded-lg bg-blue-600 px-4 py-1.5 text-sm font-medium text-white transition hover:bg-blue-700"
              >
                Entrar
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
