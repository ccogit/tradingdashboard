import { useOrders } from '../../hooks/useOrders'
import { formatCurrency } from '../../lib/format'

export function FilledOrdersTable({ status }: { status: string }) {
  const { data: orders = [] } = useOrders(status)

  if (orders.length === 0) {
    return <div className="text-center py-8 text-muted-foreground">No {status} orders</div>
  }

  return (
    <div className="rounded-md border border-border overflow-hidden mt-4">
      <table className="w-full text-sm">
        <thead className="bg-secondary">
          <tr>
            <th className="text-left p-3">Time</th>
            <th className="text-left p-3">Symbol</th>
            <th className="text-left p-3">Side</th>
            <th className="text-right p-3">Qty Filled</th>
            <th className="text-right p-3">Avg Fill</th>
            <th className="text-right p-3">Commission</th>
            <th className="text-left p-3">Status</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id} className="border-t border-border hover:bg-secondary/50">
              <td className="p-3 text-muted-foreground">{new Date(o.created_at).toLocaleString()}</td>
              <td className="p-3 font-medium">{o.symbol}</td>
              <td className={`p-3 font-medium ${o.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>{o.side}</td>
              <td className="p-3 text-right">{o.filled_quantity}</td>
              <td className="p-3 text-right">{o.avg_fill_price ? formatCurrency(o.avg_fill_price) : '-'}</td>
              <td className="p-3 text-right">{o.commission ? formatCurrency(o.commission) : '-'}</td>
              <td className="p-3">
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  o.status === 'filled' ? 'bg-green-500/20 text-green-400' : 'bg-secondary text-muted-foreground'
                }`}>{o.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
