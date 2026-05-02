import { useQuery } from '@tanstack/react-query'
import { useAuthFetch } from './useAuthFetch'
import { useTradingModeStore } from '../stores/tradingModeStore'
import type { PortfolioSummary, Position } from '../types/api'

export function usePortfolioSummary() {
  const fetch = useAuthFetch()
  const accountId = useTradingModeStore((s) => s.accountId)

  return useQuery<PortfolioSummary>({
    queryKey: ['portfolio', 'summary', accountId],
    queryFn: () => fetch(`/portfolio/summary?account_id=${accountId}`),
    enabled: !!accountId,
    refetchInterval: 30_000,
  })
}

export function usePositions() {
  const fetch = useAuthFetch()
  const accountId = useTradingModeStore((s) => s.accountId)

  return useQuery<Position[]>({
    queryKey: ['portfolio', 'positions', accountId],
    queryFn: () => fetch(`/portfolio/positions?account_id=${accountId}`),
    enabled: !!accountId,
    refetchInterval: 30_000,
  })
}
