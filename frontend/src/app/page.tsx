import Link from "next/link"

export default function Home() {
  return (
    <main className="flex min-h-[calc(100vh-65px)] items-center justify-center px-6">
      <div className="w-full max-w-3xl rounded-2xl border border-slate-800 bg-slate-900 p-10 shadow-2xl">
        <span className="mb-6 inline-block rounded-full bg-blue-500/10 px-4 py-2 text-sm text-blue-400">
          Sistema FastAPI + Next.js
        </span>

        <h1 className="mb-4 text-4xl font-bold">Bem-vindo ao sistema</h1>

        <p className="mb-8 text-lg text-slate-400">
          Gerencie suas tarefas com autenticação segura e API FastAPI.
        </p>

        <div className="flex gap-4">
          <Link
            href="/dashboard"
            className="rounded-xl bg-blue-600 px-6 py-3 font-semibold transition hover:bg-blue-700"
          >
            Ir para o Dashboard
          </Link>
          <Link
            href="/login"
            className="rounded-xl border border-slate-700 px-6 py-3 font-semibold transition hover:bg-slate-800"
          >
            Fazer login
          </Link>
        </div>
      </div>
    </main>
  )
}
