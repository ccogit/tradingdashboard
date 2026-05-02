import { AccountSummaryGrid } from '../components/portfolio/AccountSummaryGrid'
import { PnLSparkline } from '../components/portfolio/PnLSparkline'
import { AllocationDonut } from '../components/portfolio/AllocationDonut'
import { PositionsTable } from '../components/positions/PositionsTable'
import { usePositions } from '../hooks/usePortfolio'

export function DashboardPage() {
  const { data: positions = [] } = usePositions()
  const top5 = positions.slice(0, 5)

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
      <AccountSummaryGrid />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <PnLSparkline />
        </div>
        <AllocationDonut />
      </div>
      <div>
        <h2 className="text-lg font-medium mb-3">Top Positions</h2>
        <PositionsTable positions={top5} compact />
      </div>
    </div>
  )
}
