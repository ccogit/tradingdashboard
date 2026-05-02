export interface PortfolioSummary {
  account_id: string
  net_liquidation: number
  total_cash: number
  buying_power: number
  excess_liquidity: number
  maintenance_margin: number
  day_pnl: number
  unrealized_pnl: number
  realized_pnl: number
  positions_count: number
  as_of: string
}

export interface Position {
  account_id: string
  conid: number
  symbol: string
  sec_type: string
  exchange: string
  currency: string
  quantity: number
  avg_cost: number
  market_price: number
  market_value: number
  unrealized_pnl: number
  realized_pnl: number
  day_pnl: number
  pct_of_nav: number
}

export interface Order {
  id: string
  client_order_id: string
  ib_order_id: number | null
  account_id: string
  conid: number
  symbol: string
  side: 'BUY' | 'SELL'
  quantity: number
  order_type: 'MKT' | 'LMT'
  limit_price: number | null
  tif: string
  outside_rth: boolean
  status: string
  filled_quantity: number
  avg_fill_price: number | null
  commission: number | null
  reject_reason: string | null
  created_at: string
  updated_at: string
}

export interface OrderCreate {
  account_id: string
  symbol?: string
  conid?: number
  sec_type?: string
  exchange?: string
  currency?: string
  side: 'BUY' | 'SELL'
  quantity: number
  order_type: 'MKT' | 'LMT'
  limit_price?: number
  tif?: string
  outside_rth?: boolean
}

export interface Contract {
  conid: number
  symbol: string
  sec_type: string
  exchange: string
  primary_exchange?: string
  currency: string
  local_symbol?: string
  description?: string
}

export interface QuoteTick {
  conid: number
  bid?: number
  ask?: number
  last?: number
  bid_size?: number
  ask_size?: number
  volume?: number
  ts: string
}

export interface WhatIfResult {
  initial_margin: number
  maintenance_margin: number
  equity_with_loan: number
  commission: number
  currency: string
  warning_text?: string
}

export interface ChatSession {
  id: string
  title: string
  last_message_at: string
  created_at: string
}

export interface Account {
  id: string
  ib_account_id: string
  alias: string
  currency: string
  type: 'paper' | 'live'
}

export interface User {
  id: string
  clerk_user_id: string
  email: string
  name: string | null
  trading_mode: string
  accounts: Account[]
}
