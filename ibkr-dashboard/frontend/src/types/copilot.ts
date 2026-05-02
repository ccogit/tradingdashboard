import type { OrderCreate } from './api'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface ToolCallData {
  tool_call_id: string
  name: string
  input: unknown
  output?: unknown
  is_error?: boolean
}

export interface StagedOrder {
  staged_order_id: string
  order: OrderCreate
}
