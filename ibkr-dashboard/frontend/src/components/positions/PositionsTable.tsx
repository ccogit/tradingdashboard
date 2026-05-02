import type { Position } from '../../types/api'
import { formatCurrency, formatPercent } from '../../lib/format'

interface Props {
  positions: Position[]
  compact?: boolean
}

export function PositionsTable({ positions, compact = false }: Props) {
  if (positions.length === 0) {
    return <div className="text-center py-8 text-muted-foreground">No open positions</div>
  }

  return (
    <div className="rounded-md border border-border overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-secondary">
          <tr>
            <th className="text-left p-3">Symbol</th>
            <th className="text-right p-3">Qty</th>
            <th className="text-right p-3">Avg Cost</th>
            <th className="text-right p-3">Mark</th>
            <th className="text-right p-3">Mkt Value</th>
            <th className="text-right p-3">Unr. P&L</th>
            {!compact && <th className="text-right p-3">Day P&L</th>}
          </tr>
        </thead>
        <tbody>
          {positions.map((p) => (
            <tr key={`${p.conid}-${p.account_id}`} className="border-t border-border hover:bg-secondary/50">
              <td className="p-3 font-medium">
                <div>{p.symbol}</div>
                <div className="text-xs text-muted-foreground">{p.sec_type}</div>
              </td>
              <td className="p-3 text-right">{p.quantity}</td>
              <td className="p-3 text-right">{formatCurrency(p.avg_cost)}</td>
              <td className="p-3 text-right">{formatCurrency(p.market_price)}</td>
              <td className="p-3 text-right">{formatCurrency(p.market_value)}</td>
              <td className={`p-3 text-right ${p.unrealized_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {formatCurrency(p.unrealized_pnl)}
              </td>
              {!compact && (
                <td className={`p-3 text-right ${p.day_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {formatCurrency(p.day_pnl)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
