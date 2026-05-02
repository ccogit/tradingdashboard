import { useOrders } from '../hooks/useOrders'
import { formatCurrency } from '../lib/format'

export function HistoryPage() {
  const { data: orders = [] } = useOrders('filled')

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Trade History</h1>
      <div className="rounded-md border border-border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-secondary">
            <tr>
              <th className="text-left p-3">Time</th>
              <th className="text-left p-3">Symbol</th>
              <th className="text-left p-3">Side</th>
              <th className="text-right p-3">Qty</th>
              <th className="text-right p-3">Avg Fill</th>
              <th className="text-right p-3">Commission</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id} className="border-t border-border hover:bg-secondary/50">
                <td className="p-3 text-muted-foreground">{new Date(o.created_at).toLocaleString()}</td>
                <td className="p-3 font-medium">{o.symbol}</td>
                <td className={`p-3 font-medium ${o.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>{o.side}</td>
                <td className="p-3 text-right">{o.quantity}</td>
                <td className="p-3 text-right">{o.avg_fill_price ? formatCurrency(o.avg_fill_price) : '-'}</td>
                <td className="p-3 text-right">{o.commission ? formatCurrency(o.commission) : '-'}</td>
              </tr>
            ))}
            {orders.length === 0 && (
              <tr><td colSpan={6} className="p-6 text-center text-muted-foreground">No filled orders found</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
