import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuthFetch } from './useAuthFetch'
import { useTradingModeStore } from '../stores/tradingModeStore'
import type { Order, OrderCreate } from '../types/api'

export function useOrders(status?: string) {
  const fetch = useAuthFetch()
  const accountId = useTradingModeStore((s) => s.accountId)

  return useQuery<Order[]>({
    queryKey: ['orders', accountId, status],
    queryFn: () => fetch(`/orders?account_id=${accountId}${status ? `&status=${status}` : ''}`),
    enabled: !!accountId,
    refetchInterval: 10_000,
  })
}

export function usePlaceOrder() {
  const fetch = useAuthFetch()
  const qc = useQueryClient()

  return useMutation<Order, Error, OrderCreate>({
    mutationFn: (body) => fetch('/orders', { method: 'POST', body: JSON.stringify(body) }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['orders'] }),
  })
}

export function useCancelOrder() {
  const fetch = useAuthFetch()
  const qc = useQueryClient()

  return useMutation<Order, Error, string>({
    mutationFn: (orderId) => fetch(`/orders/${orderId}`, { method: 'DELETE' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['orders'] }),
  })
}

export function usePreviewOrder() {
  const fetch = useAuthFetch()
  return useMutation({
    mutationFn: (body: OrderCreate) => fetch('/orders/preview', { method: 'POST', body: JSON.stringify(body) }),
  })
}
