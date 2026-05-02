import { create } from 'zustand'
import type { ChatMessage, StagedOrder } from '../types/copilot'

interface CopilotStore {
  messages: ChatMessage[]
  stagedOrders: StagedOrder[]
  sessionId: string | null
  addMessage: (msg: ChatMessage) => void
  addStagedOrder: (order: StagedOrder) => void
  removeStagedOrder: (id: string) => void
  setSessionId: (id: string) => void
  reset: () => void
}

export const useCopilotStore = create<CopilotStore>((set) => ({
  messages: [],
  stagedOrders: [],
  sessionId: null,
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  addStagedOrder: (order) => set((s) => ({ stagedOrders: [...s.stagedOrders, order] })),
  removeStagedOrder: (id) => set((s) => ({ stagedOrders: s.stagedOrders.filter((o) => o.staged_order_id !== id) })),
  setSessionId: (sessionId) => set({ sessionId }),
  reset: () => set({ messages: [], stagedOrders: [], sessionId: null }),
}))
