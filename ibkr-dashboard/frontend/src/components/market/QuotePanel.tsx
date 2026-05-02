import { useQuery } from '@tanstack/react-query'
import { useAuthFetch } from '../../hooks/useAuthFetch'
import { formatCurrency, formatNumber } from '../../lib/format'
import type { QuoteTick } from '../../types/api'

export function QuotePanel({ conid }: { conid: number }) {
  const fetch = useAuthFetch()

  const { data: quote } = useQuery<QuoteTick>({
    queryKey: ['quote', conid],
    queryFn: () => fetch(`/market/quote/${conid}`),
    refetchInterval: 5000,
  })

  if (!quote) return null

  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <div className="text-muted-foreground mb-1">Bid</div>
          <div className="text-lg font-semibold text-green-400">{quote.bid ? formatCurrency(quote.bid) : '-'}</div>
          <div className="text-xs text-muted-foreground">{quote.bid_size ?? '-'}</div>
        </div>
        <div className="text-center">
          <div className="text-muted-foreground mb-1">Last</div>
          <div className="text-lg font-semibold text-foreground">{quote.last ? formatCurrency(quote.last) : '-'}</div>
        </div>
        <div className="text-right">
          <div className="text-muted-foreground mb-1">Ask</div>
          <div className="text-lg font-semibold text-red-400">{quote.ask ? formatCurrency(quote.ask) : '-'}</div>
          <div className="text-xs text-muted-foreground">{quote.ask_size ?? '-'}</div>
        </div>
      </div>
      {quote.volume && (
        <div className="mt-2 text-xs text-muted-foreground">Volume: {formatNumber(quote.volume, 0)}</div>
      )}
    </div>
  )
}
