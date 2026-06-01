import type { User } from "../types"

const API_URL = process.env.NEXT_PUBLIC_API_URL!

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  let token: string | null = null

  if (typeof window !== "undefined") {
    token = localStorage.getItem("token")
  }

  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    ...options,
  })

  if (!res.ok) {
    throw new Error(`Erro na requisição: ${res.status}`)
  }

  return res.json()
}

export async function getUsers(): Promise<User[]> {
  const data = await apiRequest<{ users: User[] }>("/users/")
  return data.users
}
