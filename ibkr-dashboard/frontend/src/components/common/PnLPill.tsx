import { cn } from '../../lib/utils'
import { formatCurrency } from '../../lib/format'

export function PnLPill({ value, className }: { value: number; className?: string }) {
  const isPositive = value >= 0
  return (
    <span className={cn(
      'inline-flex items-center gap-1 text-sm font-medium',
      isPositive ? 'text-green-400' : 'text-red-400',
      className
    )}>
      {isPositive ? '▲' : '▼'} {formatCurrency(Math.abs(value))}
    </span>
  )
}
