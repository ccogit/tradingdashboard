import { useOrders, useCancelOrder } from '../../hooks/useOrders'
import { formatCurrency } from '../../lib/format'

export function OpenOrdersTable() {
  const { data: orders = [] } = useOrders('working')
  const cancel = useCancelOrder()

  if (orders.length === 0) {
    return <div className="text-center py-8 text-muted-foreground">No open orders</div>
  }

  return (
    <div className="rounded-md border border-border overflow-hidden mt-4">
      <table className="w-full text-sm">
        <thead className="bg-secondary">
          <tr>
            <th className="text-left p-3">Time</th>
            <th className="text-left p-3">Symbol</th>
            <th className="text-left p-3">Side</th>
            <th className="text-right p-3">Qty</th>
            <th className="text-left p-3">Type</th>
            <th className="text-right p-3">Limit</th>
            <th className="text-left p-3">TIF</th>
            <th className="text-left p-3">Status</th>
            <th className="p-3"></th>
          </tr>
        </thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id} className="border-t border-border hover:bg-secondary/50">
              <td className="p-3 text-muted-foreground">{new Date(o.created_at).toLocaleTimeString()}</td>
              <td className="p-3 font-medium">{o.symbol}</td>
              <td className={`p-3 font-medium ${o.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>{o.side}</td>
              <td className="p-3 text-right">{o.quantity}</td>
              <td className="p-3">{o.order_type}</td>
              <td className="p-3 text-right">{o.limit_price ? formatCurrency(o.limit_price) : '-'}</td>
              <td className="p-3">{o.tif}</td>
              <td className="p-3">
                <span className="text-xs px-2 py-0.5 rounded-full bg-secondary text-muted-foreground">{o.status}</span>
              </td>
              <td className="p-3">
                <button
                  onClick={() => cancel.mutate(o.id)}
                  className="text-xs text-destructive hover:underline"
                  disabled={cancel.isPending}
                >
                  Cancel
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
