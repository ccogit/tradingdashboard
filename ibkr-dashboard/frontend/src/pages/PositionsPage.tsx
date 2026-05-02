import { usePositions } from '../hooks/usePortfolio'
import { PositionsTable } from '../components/positions/PositionsTable'

export function PositionsPage() {
  const { data: positions = [], isLoading } = usePositions()

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Positions</h1>
      {isLoading ? (
        <div className="text-muted-foreground">Loading positions...</div>
      ) : (
        <PositionsTable positions={positions} />
      )}
    </div>
  )
}
