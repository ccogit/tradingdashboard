import { useUser } from '@clerk/clerk-react'
import { useTradingModeStore } from '../stores/tradingModeStore'

export function SettingsPage() {
  const { user } = useUser()
  const { mode, setMode } = useTradingModeStore()

  return (
    <div className="p-6 space-y-6 max-w-2xl">
      <h1 className="text-2xl font-semibold">Settings</h1>

      <div className="rounded-lg border border-border p-6 space-y-4">
        <h2 className="text-lg font-medium">Account</h2>
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">Email: {user?.primaryEmailAddress?.emailAddress}</p>
          <p className="text-sm text-muted-foreground">Name: {user?.fullName}</p>
        </div>
      </div>

      <div className="rounded-lg border border-border p-6 space-y-4">
        <h2 className="text-lg font-medium">Trading Mode</h2>
        <div className="flex gap-3">
          <button
            onClick={() => setMode('paper')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              mode === 'paper'
                ? 'bg-primary text-primary-foreground'
                : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
            }`}
          >
            Paper Trading
          </button>
          <button
            onClick={() => {
              if (confirm('Switch to live trading? Real money will be at risk.')) {
                setMode('live')
              }
            }}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              mode === 'live'
                ? 'bg-destructive text-destructive-foreground'
                : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
            }`}
          >
            Live Trading
          </button>
        </div>
        {mode === 'live' && (
          <p className="text-sm text-destructive">⚠ Live trading is active. Real money is at risk.</p>
        )}
      </div>
    </div>
  )
}
