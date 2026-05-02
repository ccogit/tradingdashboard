import { Card, Metric, Text } from '@tremor/react'
import { usePortfolioSummary } from '../../hooks/usePortfolio'
import { formatCurrency } from '../../lib/format'

export function BuyingPowerCard() {
  const { data } = usePortfolioSummary()

  return (
    <Card className="bg-card border-border">
      <Text className="text-muted-foreground">Buying Power</Text>
      <Metric className="text-foreground">{formatCurrency(data?.buying_power ?? 0)}</Metric>
      <Text className="text-xs text-muted-foreground mt-1">
        Excess: {formatCurrency(data?.excess_liquidity ?? 0)}
      </Text>
    </Card>
  )
}
