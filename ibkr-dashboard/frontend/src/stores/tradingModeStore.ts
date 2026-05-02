import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface TradingModeStore {
  mode: 'paper' | 'live'
  accountId: string | null
  setMode: (mode: 'paper' | 'live') => void
  setAccountId: (id: string) => void
}

export const useTradingModeStore = create<TradingModeStore>()(
  persist(
    (set) => ({
      mode: 'paper',
      accountId: null,
      setMode: (mode) => set({ mode }),
      setAccountId: (accountId) => set({ accountId }),
    }),
    { name: 'trading-mode' }
  )
)
