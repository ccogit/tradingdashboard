import { UserButton } from '@clerk/clerk-react'
import { ConnectionBadge } from './ConnectionBadge'
import { useTradingModeStore } from '../stores/tradingModeStore'

export function TopBar() {
  const mode = useTradingModeStore((s) => s.mode)

  return (
    <header className="h-14 border-b border-border bg-card flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <ConnectionBadge />
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
          mode === 'live' ? 'bg-destructive/20 text-destructive' : 'bg-muted text-muted-foreground'
        }`}>
          {mode === 'live' ? 'LIVE' : 'PAPER'}
        </span>
      </div>
      <UserButton afterSignOutUrl="/sign-in" />
    </header>
  )
}
