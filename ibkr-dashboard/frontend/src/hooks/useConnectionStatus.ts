import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuthFetch } from './useAuthFetch'
import { useConnectionStore } from '../stores/connectionStore'

export function useConnectionStatus() {
  const fetch = useAuthFetch()
  const setIbState = useConnectionStore((s) => s.setIbState)

  const query = useQuery({
    queryKey: ['health', 'ib'],
    queryFn: () => fetch<{ connected: boolean }>('/health/ib'),
    refetchInterval: 15_000,
  })

  useEffect(() => {
    if (query.data) {
      setIbState(query.data.connected ? 'connected' : 'disconnected')
    }
  }, [query.data, setIbState])

  return query
}
