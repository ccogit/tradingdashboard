import { NetLiquidityCard } from './NetLiquidityCard'
import { DailyPnLCard } from './DailyPnLCard'
import { BuyingPowerCard } from './BuyingPowerCard'
import { Card, Metric, Text } from '@tremor/react'
import { usePortfolioSummary } from '../../hooks/usePortfolio'
import { formatCurrency } from '../../lib/format'

export function AccountSummaryGrid() {
  const { data } = usePortfolioSummary()

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <NetLiquidityCard />
      <DailyPnLCard />
      <BuyingPowerCard />
      <Card className="bg-card border-border">
        <Text className="text-muted-foreground">Unrealized P&L</Text>
        <Metric className={`${(data?.unrealized_pnl ?? 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
          {formatCurrency(data?.unrealized_pnl ?? 0)}
        </Metric>
      </Card>
    </div>
  )
}
