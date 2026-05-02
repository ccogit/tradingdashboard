import { Card, DonutChart, Title, Legend } from '@tremor/react'
import { usePositions } from '../../hooks/usePortfolio'
import { formatCurrency } from '../../lib/format'

export function AllocationDonut() {
  const { data: positions = [] } = usePositions()

  const data = positions
    .filter((p) => p.market_value > 0)
    .sort((a, b) => b.market_value - a.market_value)
    .slice(0, 8)
    .map((p) => ({ name: p.symbol, value: p.market_value }))

  return (
    <Card className="bg-card border-border">
      <Title className="text-foreground">Allocation</Title>
      <DonutChart
        className="mt-4 h-40"
        data={data}
        index="name"
        category="value"
        valueFormatter={formatCurrency}
        showAnimation={false}
      />
    </Card>
  )
}
