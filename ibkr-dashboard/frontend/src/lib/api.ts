import { env } from './env'

class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message)
  }
}

async function getToken(): Promise<string | null> {
  try {
    const { useAuth } = await import('@clerk/clerk-react')
    return null
  } catch {
    return null
  }
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit & { token?: string } = {}
): Promise<T> {
  const { token, ...rest } = options
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(rest.headers as Record<string, string>),
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${env.apiUrl}${path}`, { ...rest, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new ApiError(res.status, body.code || 'UNKNOWN', body.message || res.statusText)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}
