import { Card, Metric, Text } from '@tremor/react'
import { usePortfolioSummary } from '../../hooks/usePortfolio'
import { formatCurrency, formatPercent } from '../../lib/format'

export function DailyPnLCard() {
  const { data } = usePortfolioSummary()
  const pnl = data?.day_pnl ?? 0
  const isPositive = pnl >= 0

  return (
    <Card className="bg-card border-border">
      <Text className="text-muted-foreground">Daily P&L</Text>
      <Metric className={isPositive ? 'text-green-400' : 'text-red-400'}>
        {isPositive ? '+' : ''}{formatCurrency(pnl)}
      </Metric>
    </Card>
  )
}
