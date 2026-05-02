import { create } from 'zustand'

type ConnectionState = 'connecting' | 'connected' | 'disconnected' | 'error'

interface ConnectionStore {
  ibState: ConnectionState
  wsState: ConnectionState
  setIbState: (state: ConnectionState) => void
  setWsState: (state: ConnectionState) => void
}

export const useConnectionStore = create<ConnectionStore>((set) => ({
  ibState: 'connecting',
  wsState: 'disconnected',
  setIbState: (ibState) => set({ ibState }),
  setWsState: (wsState) => set({ wsState }),
}))
