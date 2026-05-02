import { usePlaceOrder } from '../../hooks/useOrders'
import { useCopilotStore } from '../../stores/copilotStore'
import { formatCurrency } from '../../lib/format'
import type { StagedOrder } from '../../types/copilot'

export function StagedOrderCard({ stagedOrder }: { stagedOrder: StagedOrder }) {
  const placeOrder = usePlaceOrder()
  const removeStagedOrder = useCopilotStore((s) => s.removeStagedOrder)
  const { order } = stagedOrder

  async function confirm() {
    await placeOrder.mutateAsync(order)
    removeStagedOrder(stagedOrder.staged_order_id)
  }

  return (
    <div className="rounded-lg border border-primary/30 bg-primary/5 p-4 space-y-3">
      <div className="text-sm font-medium text-primary">Staged Order — Awaiting Confirmation</div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div><span className="text-muted-foreground">Symbol:</span> <span className="font-medium">{order.symbol}</span></div>
        <div><span className="text-muted-foreground">Side:</span> <span className={`font-medium ${order.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>{order.side}</span></div>
        <div><span className="text-muted-foreground">Qty:</span> <span className="font-medium">{order.quantity}</span></div>
        <div><span className="text-muted-foreground">Type:</span> <span className="font-medium">{order.order_type}</span></div>
        {order.limit_price && <div><span className="text-muted-foreground">Limit:</span> <span className="font-medium">{formatCurrency(order.limit_price)}</span></div>}
      </div>
      <div className="flex gap-2">
        <button
          onClick={confirm}
          disabled={placeOrder.isPending}
          className="flex-1 py-2 rounded-md text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
        >
          {placeOrder.isPending ? 'Placing...' : 'Confirm & Place'}
        </button>
        <button
          onClick={() => removeStagedOrder(stagedOrder.staged_order_id)}
          className="px-4 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground bg-secondary"
        >
          Cancel
        </button>
      </div>
    </div>
  )
}
