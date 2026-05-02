import { useState } from 'react'
import { TradeTicket } from '../components/trade/TradeTicket'
import { QuotePanel } from '../components/market/QuotePanel'
import type { Contract } from '../types/api'

export function TradePage() {
  const [selectedContract, setSelectedContract] = useState<Contract | null>(null)

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Trade</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-4">
          {selectedContract && <QuotePanel conid={selectedContract.conid} />}
        </div>
        <TradeTicket onContractSelect={setSelectedContract} />
      </div>
    </div>
  )
}
