import { Card, AreaChart, Title } from '@tremor/react'
import { useQuery } from '@tanstack/react-query'
import { useAuthFetch } from '../../hooks/useAuthFetch'
import { useTradingModeStore } from '../../stores/tradingModeStore'
import { formatCurrency } from '../../lib/format'

export function PnLSparkline() {
  const fetch = useAuthFetch()
  const accountId = useTradingModeStore((s) => s.accountId)

  const { data } = useQuery({
    queryKey: ['portfolio', 'pnl', accountId, '1d'],
    queryFn: () => fetch<{ points: { ts: string; equity: number; pnl: number }[] }>(`/portfolio/pnl?account_id=${accountId}&range=1d`),
    enabled: !!accountId,
  })

  const chartData = (data?.points ?? []).map((p) => ({
    time: new Date(p.ts).toLocaleTimeString(),
    Equity: p.equity,
    'P&L': p.pnl,
  }))

  return (
    <Card className="bg-card border-border">
      <Title className="text-foreground">Portfolio Value (Today)</Title>
      <AreaChart
        className="mt-4 h-40"
        data={chartData}
        index="time"
        categories={['Equity']}
        colors={['blue']}
        valueFormatter={formatCurrency}
        showLegend={false}
        showXAxis={false}
        showGridLines={false}
      />
    </Card>
  )
}
