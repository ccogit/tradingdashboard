import type { QuoteTick, Order } from './api'

export type WSEvent =
  | { type: 'tick'; payload: QuoteTick }
  | { type: 'order_status'; payload: Order }
  | { type: 'execution'; payload: unknown }
  | { type: 'account_value'; payload: { key: string; value: string; currency: string; account_id: string } }
  | { type: 'pnl'; payload: { daily_pnl: number; unrealized_pnl: number; realized_pnl: number } }
  | { type: 'pong' }
