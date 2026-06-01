interface LoginData {
  email: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

export async function login(data: LoginData): Promise<LoginResponse> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: data.email, password: data.password }),
  })

  if (!res.ok) throw new Error(`Erro: ${res.status}`)
  return res.json()
}

export function logout() {
  localStorage.removeItem("token")
  document.cookie = "token=; path=/; max-age=0"
}
