import { useAuth } from '@clerk/clerk-react'
import { apiFetch } from '../lib/api'

export function useAuthFetch() {
  const { getToken } = useAuth()

  return async function authFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = await getToken()
    return apiFetch<T>(path, { ...options, token: token ?? undefined })
  }
}
