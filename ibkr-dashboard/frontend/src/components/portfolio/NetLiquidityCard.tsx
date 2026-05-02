import { Card, Metric, Text, Flex, BadgeDelta } from '@tremor/react'
import { usePortfolioSummary } from '../../hooks/usePortfolio'
import { formatCurrency } from '../../lib/format'

export function NetLiquidityCard() {
  const { data, isLoading } = usePortfolioSummary()

  return (
    <Card className="bg-card border-border">
      <Text className="text-muted-foreground">Net Liquidation</Text>
      {isLoading ? (
        <div className="h-8 mt-2 bg-secondary rounded animate-pulse" />
      ) : (
        <Metric className="text-foreground">{formatCurrency(data?.net_liquidation ?? 0)}</Metric>
      )}
    </Card>
  )
}
