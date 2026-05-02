import { create } from 'zustand'
import type { QuoteTick } from '../types/api'

interface QuotesStore {
  quotes: Record<number, QuoteTick>
  updateQuote: (tick: QuoteTick) => void
}

export const useQuotesStore = create<QuotesStore>((set) => ({
  quotes: {},
  updateQuote: (tick) =>
    set((state) => ({ quotes: { ...state.quotes, [tick.conid]: tick } })),
}))
