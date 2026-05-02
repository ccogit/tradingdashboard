import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { SymbolSearch } from './SymbolSearch'
import { usePlaceOrder, usePreviewOrder } from '../../hooks/useOrders'
import { useTradingModeStore } from '../../stores/tradingModeStore'
import { formatCurrency } from '../../lib/format'
import type { Contract } from '../../types/api'

const schema = z.object({
  side: z.enum(['BUY', 'SELL']),
  quantity: z.number().positive(),
  order_type: z.enum(['MKT', 'LMT']),
  limit_price: z.number().optional(),
  tif: z.enum(['DAY', 'GTC', 'IOC']),
  outside_rth: z.boolean(),
})

type FormData = z.infer<typeof schema>

interface Props {
  onContractSelect?: (contract: Contract) => void
}

export function TradeTicket({ onContractSelect }: Props) {
  const [contract, setContract] = useState<Contract | null>(null)
  const [showPreview, setShowPreview] = useState(false)
  const accountId = useTradingModeStore((s) => s.accountId)
  const placeOrder = usePlaceOrder()
  const previewOrder = usePreviewOrder()

  const { register, handleSubmit, watch, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { side: 'BUY', order_type: 'MKT', tif: 'DAY', outside_rth: false, quantity: 1 },
  })

  const orderType = watch('order_type')
  const side = watch('side')

  function handleContractSelect(c: Contract) {
    setContract(c)
    onContractSelect?.(c)
  }

  async function onSubmit(data: FormData) {
    if (!contract || !accountId) return
    if (!showPreview) {
      await previewOrder.mutateAsync({ ...data, account_id: accountId, conid: contract.conid, symbol: contract.symbol })
      setShowPreview(true)
      return
    }
    await placeOrder.mutateAsync({ ...data, account_id: accountId, conid: contract.conid, symbol: contract.symbol })
    setShowPreview(false)
  }

  return (
    <div className="rounded-lg border border-border bg-card p-6 space-y-4">
      <h2 className="text-lg font-semibold">Trade Ticket</h2>

      <SymbolSearch onSelect={handleContractSelect} />

      {contract && (
        <div className="text-sm text-muted-foreground">
          Selected: <span className="text-foreground font-medium">{contract.symbol}</span> — {contract.description}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Side */}
        <div className="flex gap-2">
          {(['BUY', 'SELL'] as const).map((s) => (
            <label key={s} className="flex-1">
              <input type="radio" value={s} {...register('side')} className="sr-only" />
              <span className={`block text-center py-2 rounded-md text-sm font-medium cursor-pointer transition-colors ${
                side === s
                  ? s === 'BUY' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                  : 'bg-secondary text-muted-foreground hover:bg-secondary/80'
              }`}>{s}</span>
            </label>
          ))}
        </div>

        {/* Order type */}
        <div className="flex gap-2">
          {(['MKT', 'LMT'] as const).map((t) => (
            <label key={t} className="flex-1">
              <input type="radio" value={t} {...register('order_type')} className="sr-only" />
              <span className={`block text-center py-2 rounded-md text-sm font-medium cursor-pointer transition-colors ${
                orderType === t ? 'bg-primary text-primary-foreground' : 'bg-secondary text-muted-foreground'
              }`}>{t}</span>
            </label>
          ))}
        </div>

        {/* Quantity */}
        <div>
          <label className="block text-sm text-muted-foreground mb-1">Quantity</label>
          <input
            type="number"
            min={1}
            step={1}
            {...register('quantity', { valueAsNumber: true })}
            className="w-full bg-secondary border border-border rounded-md px-3 py-2 text-sm"
          />
        </div>

        {/* Limit price */}
        {orderType === 'LMT' && (
          <div>
            <label className="block text-sm text-muted-foreground mb-1">Limit Price</label>
            <input
              type="number"
              step="0.01"
              {...register('limit_price', { valueAsNumber: true })}
              className="w-full bg-secondary border border-border rounded-md px-3 py-2 text-sm"
            />
          </div>
        )}

        {/* TIF */}
        <div>
          <label className="block text-sm text-muted-foreground mb-1">Time in Force</label>
          <select {...register('tif')} className="w-full bg-secondary border border-border rounded-md px-3 py-2 text-sm">
            <option value="DAY">Day</option>
            <option value="GTC">GTC</option>
            <option value="IOC">IOC</option>
          </select>
        </div>

        {/* Preview */}
        {showPreview && previewOrder.data && (
          <div className="rounded-md bg-secondary p-4 text-sm space-y-1">
            <div className="font-medium mb-2">Order Preview</div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Init Margin</span>
              <span>{formatCurrency(previewOrder.data.initial_margin)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Commission est.</span>
              <span>{formatCurrency(previewOrder.data.commission)}</span>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={!contract || placeOrder.isPending || previewOrder.isPending}
          className={`w-full py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50 ${
            showPreview
              ? 'bg-primary text-primary-foreground hover:bg-primary/90'
              : 'bg-secondary text-foreground hover:bg-secondary/80'
          }`}
        >
          {showPreview
            ? placeOrder.isPending ? 'Placing...' : 'Confirm & Place Order'
            : previewOrder.isPending ? 'Previewing...' : 'Preview Order'}
        </button>

        {showPreview && (
          <button type="button" onClick={() => setShowPreview(false)} className="w-full py-2 rounded-md text-sm text-muted-foreground hover:text-foreground">
            Edit
          </button>
        )}

        {placeOrder.isSuccess && (
          <div className="text-green-400 text-sm text-center">Order placed successfully!</div>
        )}
        {placeOrder.isError && (
          <div className="text-red-400 text-sm text-center">{placeOrder.error?.message}</div>
        )}
      </form>
    </div>
  )
}
