import type { Metadata } from "next"
import { AuthProvider } from "../context/AuthContext"
import { Navbar } from "../components/Navbar"
import "./globals.css"

export const metadata: Metadata = {
  title: "FastAPI Zero",
  description: "Gerenciador de tarefas com FastAPI e Next.js",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-950 text-white">
        <AuthProvider>
          <Navbar />
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
